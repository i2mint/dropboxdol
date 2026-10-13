"""DropboxFiles must accept a rootdir typed in a different case than Dropbox reports
(Dropbox paths are case-insensitive) -- no credentials needed: the client is mocked
(i2mint/dropboxdol#1)."""

from types import SimpleNamespace as NS
from unittest import mock

import pytest

import dropboxdol.base as base


def _store(rootdir, displayed_paths):
    con = mock.Mock()
    con.files_list_folder.return_value = NS(
        entries=[NS(path_display=p) for p in displayed_paths],
        cursor="c",
        has_more=False,
    )
    with mock.patch.object(base, "get_client", return_value=con):
        return base.DropboxFiles(rootdir)


@pytest.mark.parametrize("rootdir", ["/MyFolder/", "/myfolder/", "/MYFOLDER/"])
def test_rootdir_case_mismatch_lists_relative_keys(rootdir):
    s = _store(rootdir, ["/myfolder/a.txt", "/myfolder/sub/b.txt"])
    assert list(s) == ["a.txt", "sub/b.txt"]


def test_out_of_scope_ids_never_become_keys():
    """An id outside the rootdir yields no (corrupted) key: dol >= the #82 fix raises
    OutOfScopeKeyError on ``_key_of_id``, and iteration skips such ids (newer dol)."""
    from dol.errors import OutOfScopeKeyError

    s = _store("/MyFolder/", ["/elsewhere/a.txt", "/myfolder/b.txt"])
    with pytest.raises(OutOfScopeKeyError):
        s._key_of_id("/elsewhere/a.txt")
    try:
        keys = list(s)
    except OutOfScopeKeyError:  # dol that still raises from iteration
        return
    assert keys == ["b.txt"]
