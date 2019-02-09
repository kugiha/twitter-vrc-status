#!/usr/bin/env python3

from getpass import getpass

from vrchat_api import VRChatAPI
from vrchat_api.jsonObject import WorldLocation
from vrchat_api.enum import ModerationType
from vrchat_api.util import getInstanceNumberFromId

"""
Show a list of worlds where your friends are staying in descending order.
"""

a = VRChatAPI(
    getpass("VRChat Username"),
    getpass()
)
a.authenticate()

friends = a.getFriends(offline=False)
locations = set([x.location for x in friends]) - set([WorldLocation("offline"), WorldLocation("private")])
worldIds = set([x.worldId for x in locations])
worlds = dict([(x, a.getWorldById(x)) for x in worldIds])
friendsInLocations = dict([(x, list(filter(lambda y: y.location == x, friends))) for x in locations])

print()
for location, users in sorted(friendsInLocations.items(),
                              key=lambda x: len(x[1]),
                              reverse=True):
    print("{}:{}:".format(
        worlds[location.worldId].name,
        getInstanceNumberFromId(location.instanceId)
    ))
    for user in users:
        print("   {}".format(user.displayName))
