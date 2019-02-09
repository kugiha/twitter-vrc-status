#!/usr/bin/env python3

from getpass import getpass

from vrchat_api import VRChatAPI
from vrchat_api.enum import ModerationType

"""
Show a list of users who have blocked you.
"""

a = VRChatAPI(
    getpass("VRChat Username"),
    getpass()
)
a.authenticate()

moderations = a.getModerations()
blockModerations = filter(
    lambda x: x.type == ModerationType.BLOCK,
    moderations
)
unblockModerations = filter(
    lambda x: x.type == ModerationType.UNBLOCK,
    moderations
)

for m in blockModerations:
    s = "{:20} blcoked me at {} ...".format(
        m.targetDisplayName,
        m.created
    )
    unblocks = list(filter(
        lambda x: x.targetDisplayName == m.targetDisplayName,
        unblockModerations
    ))
    if len(unblocks) > 0:
        latestUnblock = unblocks[-1]
        if latestUnblock.created > m.created:
            s += " but he/she unblocked at {}".format(latestUnblock.created)

    print(s)
