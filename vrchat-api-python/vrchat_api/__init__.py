import json

import requests
from requests.auth import HTTPBasicAuth

from vrchat_api.jsonObject import User, Avatar, Moderation, World, Instance

class VRChatAPI():
    """
    An object to handle VRChat API.
    """

    URL = "https://api.vrchat.cloud/api/1"

    def __init__(self, user, pw, timeout=10):
        """
        Args:
            user (str): An username.
            pw (str): The password of the user.
            timeout (float): The length of timeout in seconds. This will passed to `requests.get`.
        """

        self.auth = HTTPBasicAuth(user, pw)
        self.apiKey = None
        self.token = None
        self.timeout = timeout

    def _updateApiKey(self):
        """
        Get the latest API key and store it to self.apiKey.
        This function is automatically invoked on authentication, so users do not have to call it.
        """
        ret = self._callApi("config", useApiKey=False)
        self.apiKey = ret["clientApiKey"]

    def _callApi(self,
                 endPoint, params={},
                 auth=None, useApiKey=True, returnCookie=False):
        """
        Call an endpoint of the VRChat API with parameters.
        This function is wrapped by other public functions, so uses do not have to call it.

        Users are responsible for handling any exceptions occured.
        """

        # print("callApi: ", endPoint)

        url = "{}/{}".format(VRChatAPI.URL, endPoint)
        if useApiKey:
            if self.apiKey is None:
                self._updateApiKey()

            params = dict(params.items())
            params["apiKey"] = self.apiKey

        for i, (k, v) in enumerate(params.items()):
            url += "{}{}={}".format(("?" if i == 0 else "&"), k, v)

        ret = requests.get(
            url,
            data={"authToken": self.token},
            auth=auth,
            timeout=self.timeout
        )

        assert ret.status_code == 200
        return ret.cookies if returnCookie else json.loads(ret.text)

    def authenticate(self):
        """
        Get an access token and store it to self.token.
        Users have to explicitly call this function before using the API.
        """

        ret = self._callApi(
            "auth/user",
            auth=self.auth,
            returnCookie=True
        )
        self.token = ret["auth"]

    def getFriends(self, offline=False, favorite=False):
        """
        Get a list of friends.

        Args:
            offline (bool): Offline friends will be returned.
            favorite (bool): Only favorite friends will be returned.
        """

        n = 100
        offset = 0
        ret = []
        while True:
            l =  self._callApi(
                "auth/user/friends"+("/favorite" if favorite else ""),
                params={
                    "n": n,
                    "offset": offset,
                    "offline": ("true" if offline else "false")
                }
            )
            if len(l) == 0:
                return [User(x) for x in ret]
            else:
                ret.extend(l)
                offset += n

    def getAvaterById(self, i):
        """
        Get information of an avatar.

        Args:
            i (str): An avatar ID.
        """

        return Avatar(self._callApi("avatars/{}".format(i)))

    def getUserById(self, i):
        """
        Get information of an user.

        Args:
            i (str): An user ID.
        """

        return User(self._callApi("users/{}".format(i)))

    def getWorldById(self, i):
        """
        Get information of a world.

        Args:
            i (str): A world ID.
        """

        return World(self._callApi("worlds/{}".format(i)))

    def getInstanceById(self, worldId, instanceId):
        """
        Get information of an instance.

        Args:
            i (str): An instance ID.
        """

        return Instance(self._callApi("worlds/{}/{}".format(worldId, instanceId)))

    def getModerations(self):
        """
        Get a list of moderations.
        """

        return [Moderation(x) for x in self._callApi("auth/user/playermoderations")]
