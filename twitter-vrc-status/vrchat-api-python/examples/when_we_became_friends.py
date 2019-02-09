#!/usr/bin/env python3

from getpass import getpass

from vrchat_api import VRChatAPI
from vrchat_api.enum import ModerationType

"""
Show a list of users and time when he/she became your friend.
"""

a = VRChatAPI(
    getpass("VRChat Username"),
    getpass()
)
a.authenticate()

moderations = a.getModerations()
unmuteModerations = filter(
    lambda x: x.type == ModerationType.UNMUTE,
    moderations
)

for m in unmuteModerations:
    print("{:20} became my friend at {}".format(
        m.targetDisplayName,
        m.created
    ))
