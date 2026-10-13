"""DropboxFiles listing (pagination, null path_display, ``id:``/``ns:`` rootdirs) and
``__contains__`` (case-insensitive) -- no credentials needed: the client is mocked
(i2mint/dropboxdol#2)."""

from types import SimpleNamespace as NS
from unittest import mock

import pytest
from dropbox.exceptions import ApiError
from dropbox.files import GetMetadataError, LookupError as DropboxLookupError

import dropboxdol.base as base


def _page(paths, *, has_more=False, cursor="c"):
    return NS(
        entries=[NS(path_display=p) for p in paths], cursor=cursor, has_more=has_more
    )


def _store(rootdir, first_page, *more_pages, cls=base.DropboxFiles, **kwargs):
    con = mock.Mock()
    con.files_list_folder.return_value = first_page
    # keyed by cursor, so that listing twice (``list`` calls ``len`` first) is repeatable
    chain = [first_page, *more_pages]
    by_cursor = {a.cursor: b for a, b in zip(chain, chain[1:])}
    con.files_list_folder_continue.side_effect = lambda cursor: by_cursor[cursor]
    with mock.patch.object(base, "get_client", return_value=con):
        return cls(rootdir, **kwargs), con


def _lookup_error(lookup_error):
    return ApiError("rid", GetMetadataError.path(lookup_error), "msg", None)


def test_pagination_follows_has_more_to_the_end():
    pages = [
        _page(["/r/a"], has_more=True, cursor="c1"),
        _page(["/r/b"], has_more=True, cursor="c2"),
        _page(["/r/c"], has_more=True, cursor="c3"),
        _page(["/r/d"]),
    ]
    s, con = _store("/r/", *pages)
    assert list(s) == ["a", "b", "c", "d"]
    assert [c.args[0] for c in con.files_list_folder_continue.call_args_list][:3] == [
        "c1",
        "c2",
        "c3",
    ]


def test_listing_uses_files_list_folder_kwargs():
    s, con = _store("/r/", _page([]))
    list(s)
    con.files_list_folder.assert_called_with(
        "/r/", recursive=True, include_non_downloadable_files=False
    )
    s, con = _store("/r/", _page([]), files_list_folder_kwargs={"recursive": False})
    list(s)
    con.files_list_folder.assert_called_with("/r/", recursive=False)


def test_null_path_display_entries_are_skipped():
    s, _ = _store(
        "/r/", _page(["/r/a", None], has_more=True), _page([None, "/r/b"], cursor="c2")
    )
    assert list(s) == ["a", "b"]


@pytest.mark.parametrize(
    "rootdir, folder_display, expected_folder_arg",
    [
        ("id:abc123", "/Team/Docs", "id:abc123"),
        ("id:abc123/", "/Team/Docs", "id:abc123"),
        ("ns:42/sub", "/Mounted/sub", "ns:42/sub"),
    ],
)
def test_id_and_ns_rootdirs_list_relative_keys(
    rootdir, folder_display, expected_folder_arg
):
    s, con = _store(
        rootdir, _page([f"{folder_display}/a.txt", f"{folder_display}/x/b"])
    )
    con.files_get_metadata.return_value = NS(path_display=folder_display)
    # a rootdir without a trailing slash yields keys that start with the separator
    keys = list(s)
    lead = "" if rootdir.endswith("/") else "/"
    assert keys == [f"{lead}a.txt", f"{lead}x/b"]
    con.files_get_metadata.assert_called_once_with(expected_folder_arg)
    list(s)  # resolved once, cached
    con.files_get_metadata.assert_called_once()
    # the API-facing key -> id mapping keeps the rootdir as given
    assert s._id_of_key(f"{lead}a.txt") == rootdir + f"{lead}a.txt"
    assert con.files_list_folder.call_args.args[0] == rootdir


def test_unresolvable_id_rootdir_raises_informative_error():
    s, con = _store("ns:42", _page(["/a"]))
    con.files_get_metadata.return_value = NS(path_display=None)
    with pytest.raises(ValueError, match="path rootdir"):
        list(s)


def test_contains_asks_server_and_is_case_insensitive_by_construction():
    s, con = _store("/MyFolder/", _page(["/myfolder/a.txt"]))
    con.files_get_metadata.return_value = NS(path_display="/myfolder/a.txt")
    assert "a.txt" in s
    con.files_get_metadata.assert_called_once_with("/MyFolder/a.txt")
    con.files_list_folder.assert_not_called()  # no full listing


@pytest.mark.parametrize(
    "lookup_error",
    [DropboxLookupError.not_found, DropboxLookupError.malformed_path(None)],
)
def test_contains_false_when_path_not_found(lookup_error):
    s, con = _store("/r/", _page([]))
    con.files_get_metadata.side_effect = _lookup_error(lookup_error)
    assert "nope" not in s
    con.files_get_metadata.assert_called_once_with("/r/nope")


def test_contains_propagates_other_errors():
    s, con = _store("/r/", _page([]))
    con.files_get_metadata.side_effect = _lookup_error(DropboxLookupError.not_file)
    with pytest.raises(ApiError):
        "x" in s
    con.files_get_metadata.side_effect = RuntimeError("network")
    with pytest.raises(RuntimeError):
        "x" in s


def test_persister_contains_false_for_non_string_keys():
    s, con = _store("/r/", _page([]), cls=base.DropboxPersister)
    assert 5 not in s
    con.files_get_metadata.assert_not_called()


@pytest.mark.parametrize(
    "cls, rootdir, key",
    [(base.DropboxFiles, "", "a.txt"), (base.DropboxPersister, "/r/", "")],
)
def test_contains_false_for_keys_that_are_not_valid_paths(cls, rootdir, key):
    """Uses a real SDK client (network methods are never reached): the SDK validates
    the path itself and raises ``ValidationError``, which isn't an ``ApiError``."""
    import dropbox

    client = dropbox.Dropbox("not-a-real-token")
    with mock.patch.object(base, "get_client", return_value=client):
        s = cls(rootdir)
    with mock.patch.object(client, "request") as request:
        assert key not in s
    request.assert_not_called()


def test_persister_contains_uses_raw_path():
    s, con = _store("/r/", _page([]), cls=base.DropboxPersister)
    con.files_get_metadata.return_value = NS()
    assert "/r/a" in s
    con.files_get_metadata.assert_called_once_with("/r/a")
