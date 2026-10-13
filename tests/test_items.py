"""DropboxFiles reads and membership errors, with the client mocked (no credentials)."""

from types import SimpleNamespace as NS
from unittest import mock

import pytest
from dropbox.exceptions import ApiError
from dropbox.files import DownloadError, GetMetadataError, LookupError as DbxLookupError

import dropboxdol.base as base


def _files(rootdir="/r/"):
    con = mock.Mock()
    with mock.patch.object(base, "get_client", return_value=con):
        return base.DropboxFiles(rootdir), con


def test_getitem_returns_the_downloaded_bytes():
    s, con = _files()
    con.files_download.return_value = (NS(), NS(status_code=200, content=b"hi"))
    assert s["/r/a.txt"] == b"hi"


def test_getitem_of_a_missing_file_is_a_keyerror():
    s, con = _files()
    con.files_download.side_effect = ApiError(
        "rid", DownloadError.path(DbxLookupError.not_found), "msg", None
    )
    with pytest.raises(KeyError):
        s["/r/nope"]


def test_contains_reraises_an_error_that_is_not_a_lookup_miss():
    s, con = _files()
    con.files_get_metadata.side_effect = ApiError(
        "rid", GetMetadataError.path(DbxLookupError.restricted_content), "msg", None
    )
    with pytest.raises(ApiError):
        "x" in s


def test_getitem_refuses_a_download_that_did_not_answer_200():
    s, con = _files()
    con.files_download.return_value = (NS(), NS(status_code=500, content=b"error page"))
    with pytest.raises(ValueError, match="HTTP 500"):
        s["/r/a.txt"]
