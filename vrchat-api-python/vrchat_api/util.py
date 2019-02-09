from datetime import datetime

def strptime(t):
    try:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S+00:00")

def getInstanceNumberFromId(instanceId):
    return instanceId.split("~")[0]
