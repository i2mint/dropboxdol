# dropboxdol.connection

Objects to connect to Dropbox.

### Functions

| `complete_config_file_with_refresh_token`(...)                                                     |                                                                                |
|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `config_file_to_dict`(config_filepath)                                                             |                                                                                |
| [`copy_config_file`](#dropboxdol.connection.copy_config_file)(src_config_file[, ...])          | Copy a configuration file from one location to another.                        |
| [`create_config_file`](#dropboxdol.connection.create_config_file)(config_file, \*, app_key, ...) | Create a configuration file for a Dropbox client.                              |
| `create_or_edit_config_file`(config_file, \*[, ...])                                               |                                                                                |
| [`get_client`](#dropboxdol.connection.get_client)([config])                              | Return a Dropbox client using the best available configuration source.         |
| [`get_client_from_args`](#dropboxdol.connection.get_client_from_args)(oauth2_access_token[, ...])  | Create a Dropbox client using explicit credentials with additional validation. |
| [`get_client_from_config_file`](#dropboxdol.connection.get_client_from_config_file)(config_filepath)      | Create a Dropbox client by loading configuration from a JSON file.             |
| [`get_client_from_environment_vars`](#dropboxdol.connection.get_client_from_environment_vars)(...[, ...])      | Create a Dropbox client using configuration from environment variables.        |
| [`get_envvar_if_upper_case_and_exists`](#dropboxdol.connection.get_envvar_if_upper_case_and_exists)(config)       | Retrieve a configuration value.                                                |
| [`get_tokens_interactive`](#dropboxdol.connection.get_tokens_interactive)(app_key, app_secret)       | Runs an interactive OAuth flow to obtain an access token and a refresh token.  |

### dropboxdol.connection.copy_config_file(src_config_file, dest_config_file=None)

Copy a configuration file from one location to another.

If the destination file already exists, a FileExistsError will be raised.

### dropboxdol.connection.create_config_file(config_file, , app_key, app_secret, oauth2_access_token=None, oauth2_refresh_token=None)

Create a configuration file for a Dropbox client.

If the file already exists, a FileExistsError will be raised.
The `config_file` must be a sring ending with ‘.json’.
If oauth2_refresh_token is not given, an interactive flow will be used to obtain it,
also replacing the oauth2_access_token.

### dropboxdol.connection.get_client(config='default_dropbox_config.json', \*\*kwargs)

Return a Dropbox client using the best available configuration source.

Priority:

> 1. If an oauth2_access_token is provided and ends with ‘.json’, load configuration from that file.
> 2. Else, if the environment variable (named by oauth2_access_token) exists, use environment variables.
> 3. Otherwise, use explicit parameters provided via kwargs.

Expected keyword arguments:

> - oauth2_access_token
> - oauth2_refresh_token
> - app_key
> - app_secret
* **Return type:**
  `Dropbox`

### dropboxdol.connection.get_client_from_args(oauth2_access_token, oauth2_refresh_token=None, app_key=None, app_secret=None)

Create a Dropbox client using explicit credentials with additional validation.

Validation includes:

> - Ensuring that oauth2_access_token is provided and is a non-empty string.
> - If any of oauth2_refresh_token, app_key, or app_secret are provided, then all must be provided
>   to enable auto-refresh.
> - Issuing soft warnings if any of the parameters appear to be environment variable names
>   (all uppercase), which might indicate that the caller intended to pass literal values.
* **Parameters:**
  * **oauth2_access_token** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The Dropbox access token.
  * **oauth2_refresh_token** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – The Dropbox refresh token.
  * **app_key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Your Dropbox app key.
  * **app_secret** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Your Dropbox app secret.
* **Returns:**
  A Dropbox client instance.
* **Return type:**
  `Dropbox`

### dropboxdol.connection.get_client_from_config_file(config_filepath)

Create a Dropbox client by loading configuration from a JSON file.

The JSON file must contain the keys:

> - “oauth2_access_token”
> - “oauth2_refresh_token”
> - “app_key”
> - “app_secret”
* **Raises:**
  * [**FileNotFoundError**](https://docs.python.org/3/builtins/exceptions.html#FileNotFoundError) – If the config file does not exist.
  * [**Exception**](https://docs.python.org/3/builtins/exceptions.html#Exception) – If required keys are missing.
* **Return type:**
  `Dropbox`

### dropboxdol.connection.get_client_from_environment_vars(oauth2_access_token, oauth2_refresh_token=None, app_key=None, app_secret=None)

Create a Dropbox client using configuration from environment variables.

The provided parameter names are interpreted as the names of the environment variables.
For example, calling:

> get_client_from_environment_vars(“DROPBOX_ACCESS_TOKEN”, “DROPBOX_REFRESH_TOKEN”,
> : “DROPBOX_APP_KEY”, “DROPBOX_APP_SECRET”)

will use the values from os.environ (if they exist), or fall back to the literal strings.

* **Return type:**
  `Dropbox`

### dropboxdol.connection.get_envvar_if_upper_case_and_exists(config)

Retrieve a configuration value.

First checks os.environ for the given key. If present, returns its value;
otherwise, returns the key itself (allowing you to pass literal values).

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### dropboxdol.connection.get_tokens_interactive(app_key, app_secret)

Runs an interactive OAuth flow to obtain an access token and a refresh token.

Ensure you pass your Dropbox app key and secret. This flow will print an
authorization URL. Visit the URL in your browser, authorize the app, then
paste the resulting code into the prompt.

* **Returns:**
  A tuple (access_token, refresh_token)
