"""Utility functions for DropboxDOL."""

import os
import re
from typing import Tuple

import dropbox
from dropbox.exceptions import ApiError, AuthError
from dropbox.sharing import SharedLinkSettings, RequestedVisibility

DFLT_ACCESS_TOKEN = "DROPBOX_ACCESS_TOKEN"  # Default key to look for in os.environ


def get_access_token(token_key: str = DFLT_ACCESS_TOKEN) -> str:
    """
    Retrieve the Dropbox access token.

    First, attempts to get the token from os.environ using the given key.
    If not found, returns the token_key itself.
    """
    env_token = os.environ.get(token_key)
    if env_token:
        return env_token
    return token_key


def get_local_full_path(path: str, dropbox_local_rootdir: str = None) -> Tuple[str, str]:
    """
    Determine the absolute local file path and the local Dropbox folder.

    If dropbox_local_rootdir is provided:
      - If path is relative, join it with dropbox_local_rootdir.
      - Otherwise, use path as is.

    If dropbox_local_rootdir is not provided:
      - If path is absolute and contains "Dropbox", infer the Dropbox folder.
      - Otherwise, raise a ValueError.

    Returns:
      A tuple (local_full_path, dropbox_local_rootdir)


    """
    if dropbox_local_rootdir is not None:
        if not os.path.isabs(path):
            local_full_path = os.path.join(dropbox_local_rootdir, path)
        else:
            local_full_path = path
    else:
        if os.path.isabs(path) and "Dropbox" in path:
            parts = path.split(os.path.sep)
            try:
                idx = parts.index("Dropbox")
            except ValueError:
                raise ValueError(
                    "Could not infer Dropbox folder from the path. Please provide dropbox_local_rootdir."
                )
            dropbox_local_rootdir = os.path.sep.join(parts[: idx + 1])
            local_full_path = path
        else:
            raise ValueError(
                "dropbox_local_rootdir not provided and the given path is not absolute or doesn't contain 'Dropbox'. Please supply dropbox_local_rootdir."
            )
    if not os.path.exists(local_full_path):
        raise FileNotFoundError(
            f"The file '{local_full_path}' does not exist. Please verify the path and dropbox_local_rootdir."
        )
    return local_full_path, dropbox_local_rootdir


def compute_dbx_file_path(local_full_path: str, dropbox_local_rootdir: str) -> str:
    """
    Compute the Dropbox file path from the local file path and the local Dropbox folder.

    The Dropbox file path is the relative path (with forward slashes) prefixed with a slash.

    >>> compute_dbx_file_path("/path/to/Dropbox/file.txt", "/path/to/Dropbox")
    '/file.txt'
    >>> compute_dbx_file_path("/path/to/Dropbox/folder/file.txt", "/path/to/Dropbox")
    '/folder/file.txt'
    """
    try:
        rel_path = os.path.relpath(local_full_path, dropbox_local_rootdir)
    except Exception as e:
        raise Exception(
            f"Failed to compute the relative Dropbox path from '{local_full_path}' and '{dropbox_local_rootdir}': {e}"
        )
    return "/" + rel_path.replace(os.path.sep, "/")


def modify_url_dl(shared_url: str, dl: int) -> str:
    """
    Adjust the Dropbox shared URL to include the desired 'dl' parameter.

    If the URL already has a 'dl' parameter, it is replaced; otherwise, the parameter
    is appended.

    >>> modify_url_dl("https://www.dropbox.com/s/abc123/file.txt?dl=0", 1)
    'https://www.dropbox.com/s/abc123/file.txt?dl=1'
    >>> modify_url_dl("https://www.dropbox.com/s/abc123/file.txt", 1)
    'https://www.dropbox.com/s/abc123/file.txt?dl=1'
    >>> modify_url_dl("https://www.dropbox.com/s/abc123/file.txt?dl=0", 0)
    'https://www.dropbox.com/s/abc123/file.txt?dl=0'
    """
    if "dl=" in shared_url:
        return re.sub(r"dl=\d", f"dl={dl}", shared_url)
    else:
        delimiter = "&" if "?" in shared_url else "?"
        return shared_url + f"{delimiter}dl={dl}"
