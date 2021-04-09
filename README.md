
# dropboxdol
dropbox with a simple (dict-like or list-like) interface


To install:	```pip install dropboxdol```


A persister for dropbox.

You need to have the python connector (if you don't: pip install dropbox)
You also need to have a token for your dropbox app. If you don't it's a google away.
Finally, for the test below, you need to put this token in ~/.py2store_configs.json' under key
dropbox.__init__kwargs, and have a folder named /py2store_data/test/ in your app space.

```python
>>> import json
>>> import os
>>> from dropboxdol import DropboxPersister
>>> configs = json.load(open(os.path.expanduser('~/.py2store_configs.json')))
>>> s = DropboxPersister('/py2store_data/test/', **configs['dropbox']['__init__kwargs'])
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
