# dropboxdol.util

Utility functions for DropboxDOL.

### Functions

| [`compute_dbx_file_path`](#dropboxdol.util.compute_dbx_file_path)(local_full_path, ...)   | Compute the Dropbox file path from the local file path and the local Dropbox folder.   |
|------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| [`get_config_val`](#dropboxdol.util.get_config_val)(config_key)                    | Retrieve a configuration value.                                                        |
| [`get_local_full_path`](#dropboxdol.util.get_local_full_path)(path[, ...])              | Determine the absolute local file path and the local Dropbox folder.                   |
| [`modify_url_dl`](#dropboxdol.util.modify_url_dl)(shared_url, dl)                 | Adjust the Dropbox shared URL to include the desired 'dl' parameter.                   |

### dropboxdol.util.compute_dbx_file_path(local_full_path, dropbox_local_rootdir)

Compute the Dropbox file path from the local file path and the local Dropbox folder.

The Dropbox file path is the relative path (with forward slashes) prefixed with a slash.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

```pycon
>>> compute_dbx_file_path("/path/to/Dropbox/file.txt", "/path/to/Dropbox")
'/file.txt'
>>> compute_dbx_file_path("/path/to/Dropbox/folder/file.txt", "/path/to/Dropbox")
'/folder/file.txt'
```

### dropboxdol.util.get_config_val(config_key)

Retrieve a configuration value.

First checks os.environ for the given key. If present, returns its value;
otherwise, returns the key itself (allowing you to pass literal values).

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### dropboxdol.util.get_local_full_path(path, dropbox_local_rootdir=None)

Determine the absolute local file path and the local Dropbox folder.

If dropbox_local_rootdir is provided:

> - If path is relative, join it with dropbox_local_rootdir.
> - Otherwise, use path as is.

If dropbox_local_rootdir is not provided:

> - If path is absolute and contains “Dropbox”, infer the Dropbox folder.
> - Otherwise, raise a ValueError.
* **Return type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  A tuple (local_full_path, dropbox_local_rootdir)

### dropboxdol.util.modify_url_dl(shared_url, dl)

Adjust the Dropbox shared URL to include the desired ‘dl’ parameter.

If the URL already has a ‘dl’ parameter, it is replaced; otherwise, the parameter
is appended.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

```pycon
>>> modify_url_dl("https://www.dropbox.com/s/abc123/file.txt?dl=0", 1)
'https://www.dropbox.com/s/abc123/file.txt?dl=1'
>>> modify_url_dl("https://www.dropbox.com/s/abc123/file.txt", 1)
'https://www.dropbox.com/s/abc123/file.txt?dl=1'
>>> modify_url_dl("https://www.dropbox.com/s/abc123/file.txt?dl=0", 0)
'https://www.dropbox.com/s/abc123/file.txt?dl=0'
```
