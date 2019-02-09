# vrchat-api-python
This is an unofficial Python library for the [VRChat API](https://vrchatapi.github.io/#/).

## How to Install
So far this library is yet to be published to PyPI.
Please run `pip3 install -e .` to install the library.

## How to Use
```python
from vrchat_api import VRChatAPI

api = VRChatAPI("YOUR_USERNAME", "YOUR_PASSWORD")
api.authenticate()

friends = api.getFriends() # A list of your friends!
```

See [`examples/`](examples/) for more details.

## Disclaimer
As mentioned in the [VRChat API Documentation](https://vrchatapi.github.io/#/), use of the API is not officially supported.
**Please use this library at your own risk**.

[VRChat](https://www.vrchat.net/) belongs to VRChat Inc.
