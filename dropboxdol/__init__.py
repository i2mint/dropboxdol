"""
Access dropbox with dict-like interface.

"""

from dropboxdol.base import (
    dropbox_link,
    DropboxFiles,
    DropboxTextFiles,
    DropboxLinkReaderWithToken,
    DropboxBinaryStore,  # deprecated: Use DropboxFiles instead
    DropboxTextStore,  # deprecated: Use DropboxTextFiles instead
)
