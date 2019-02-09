from enum import Enum

class DeveloperType(Enum):
    NONE      = 0
    TRUSTED   = 1
    INTERNAL  = 2
    MODERATOR = 3

    @staticmethod
    def fromString(developerType):
        return {
            "none":      DeveloperType.NONE,
            "trusted":   DeveloperType.TRUSTED,
            "internal":  DeveloperType.INTERNAL,
            "moderator": DeveloperType.MODERATOR
        }[developerType]

class Status(Enum):
    ACTIVE  = 0
    JOIN_ME = 1
    BUSY    = 2
    OFFLINE = 3

    @staticmethod
    def fromString(status):
        return {
            "active":  Status.ACTIVE,
            "join me": Status.JOIN_ME,
            "busy":    Status.BUSY,
            "offline": Status.OFFLINE
        }[status]

class ReleaseStatus(Enum):
    PUBLIC  = 0
    PRIVATE = 1
    HIDDEN  = 2

    @staticmethod
    def fromString(releaseStatus):
        return {
            "public":  ReleaseStatus.PUBLIC,
            "private": ReleaseStatus.PRIVATE,
            "hidden":  ReleaseStatus.HIDDEN
        }[releaseStatus]

class ModerationType(Enum):
    MUTE    = 0
    UNMUTE  = 1
    BLOCK   = 2
    UNBLOCK = 3

    @staticmethod
    def fromString(moderationType):
        return {
            "mute":    ModerationType.MUTE,
            "unmute":  ModerationType.UNMUTE,
            "block":   ModerationType.BLOCK,
            "unblock": ModerationType.UNBLOCK
        }[moderationType]
