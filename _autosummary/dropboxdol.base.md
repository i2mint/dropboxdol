# dropboxdol.base

Base functions for dropboxdol.

### Functions

| [`create_or_get_shared_link`](#dropboxdol.base.create_or_get_shared_link)(dbx, dbx_file_path)   | Create a shared link for the given Dropbox file path.                 |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| [`dropbox_link`](#dropboxdol.base.dropbox_link)(path, \*[, ...])                   | Returns a shareable Dropbox URL for the file at the given local path. |

### Classes

| [`DropboxBinaryStore`](#dropboxdol.base.DropboxBinaryStore)                              |                          |
|--------------------------------------------------------------------------------------------------|--------------------------|
| [`DropboxFiles`](#dropboxdol.base.DropboxFiles)([rootdir, connection_config, ...]) |                          |
| [`DropboxLinkReaderWithToken`](#dropboxdol.base.DropboxLinkReaderWithToken)(url[, ...])          |                          |
| [`DropboxPersister`](#dropboxdol.base.DropboxPersister)([rootdir, ...])                | A persister for dropbox. |
| [`DropboxTextFiles`](#dropboxdol.base.DropboxTextFiles)([rootdir, ...])                |                          |
| [`DropboxTextStore`](#dropboxdol.base.DropboxTextStore)                                |                          |

### dropboxdol.base.DropboxBinaryStore

alias of [`DropboxFiles`](#dropboxdol.base.DropboxFiles)

### *class* dropboxdol.base.DropboxFiles(rootdir='', , connection_config='default_dropbox_config.json', files_upload_kwargs=None, files_list_folder_kwargs=None, rev=None)

Bases: `PrefixRelativizationMixin`, `Store`, [`DropboxPersister`](#dropboxdol.base.DropboxPersister)

### *class* dropboxdol.base.DropboxLinkReaderWithToken(url, connection_config='default_dropbox_config.json', , path='', recursive=False, include_media_info=False, include_deleted=False, include_has_explicit_shared_members=False, include_mounted_folders=True, limit=None, include_property_groups=None, include_non_downloadable_files=True)

Bases: `ReadOnlyMixin`, [`DropboxPersister`](#dropboxdol.base.DropboxPersister)

### *class* dropboxdol.base.DropboxPersister(rootdir='', , connection_config='default_dropbox_config.json', files_upload_kwargs=None, files_list_folder_kwargs=None, rev=None)

Bases: `KvPersister`

A persister for dropbox.
You need to have the python connector (if you don’t: pip install dropbox)
You also need to have a token for your dropbox app. If you don’t it’s a google away.
Finally, for the test below, you need to put this token in ~/.py2store_configs.json’ under key
dropbox._\_init_\_kwargs, and have a folder named /py2store_data/test/ in your app space.

```pycon
>>> from dropboxdol.tests.test_dropbox import test_config
>>> from dropboxdol import DropboxPersister
>>> s = DropboxPersister('/py2store_data/test/', connection_config=test_config)
>>> if '/py2store_data/test/_can_remove' in s:
...     del s['/py2store_data/test/_can_remove']
...
>>>
>>> n = len(s)
>>> if n == 1:
...     assert list(s) == ['/py2store_data/test/_can_remove']
...
>>> s['/py2store_data/test/_can_remove'] = b'this is a test'
>>> assert len(s) == n + 1
>>> assert s['/py2store_data/test/_can_remove'] == b'this is a test'
>>> '/py2store_data/test/_can_remove' in s
True
>>> del s['/py2store_data/test/_can_remove']
```

### *class* dropboxdol.base.DropboxTextFiles(rootdir='', , connection_config='default_dropbox_config.json', files_upload_kwargs=None, files_list_folder_kwargs=None, rev=None)

Bases: [`DropboxFiles`](#dropboxdol.base.DropboxFiles)

### dropboxdol.base.DropboxTextStore

alias of [`DropboxTextFiles`](#dropboxdol.base.DropboxTextFiles)

### dropboxdol.base.create_or_get_shared_link(dbx, dbx_file_path)

Create a shared link for the given Dropbox file path.

If a shared link already exists, list and return the first one.
Raises an exception with detailed information on authentication errors.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### dropboxdol.base.dropbox_link(path, , dropbox_local_rootdir=None, dl=0, access_config='default_dropbox_config.json')

Returns a shareable Dropbox URL for the file at the given local path.

The function:

> 1. Retrieves the access token from os.environ using the given key or uses the provided token.
> 2. Determines the absolute local file path (using dropbox_path if needed).
> 3. Computes the Dropbox file path relative to the Dropbox folder.
> 4. Attempts to create a shared link, or retrieves an existing one if it already exists.
> 5. Modifies the URL to include the specified ‘dl’ parameter (e.g., dl=1 for direct download).
* **Parameters:**
  * **path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The file path (absolute or relative).
  * **dropbox_local_rootdir** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The local root Dropbox folder. If not provided, it will be inferred.
  * **dl** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The value for the ‘dl’ parameter in the shared URL (default is 0).
  * **access_config** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str) | [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – The access configuration (dict or file path)
* **Returns:**
  The modified shared URL.
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Raises:**
  * [**FileNotFoundError**](https://docs.python.org/3/builtins/exceptions.html#FileNotFoundError) – If the file does not exist.
  * [**Exception**](https://docs.python.org/3/builtins/exceptions.html#Exception) – For issues with path computation or Dropbox API errors.
