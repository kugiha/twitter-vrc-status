import os
import requests
from requests_oauthlib import OAuth1Session
from vrchat_api import VRChatAPI
from vrchat_api.enum import Status
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

apiKey = 'JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26'
offline_location = os.environ['offline_location']
private_location = os.environ['private_location']
name = {
    'name_template': os.environ['name_template'],
    'online_status': os.environ['online_status'],
    'offline_status': os.environ['offline_status']
}


def lambda_handler(event, context):
    is_online, location = get_vrchat_status()
    logger.info('{}, {}'.format(is_online, location))
    update_twitter_profile(is_online, location)


def update_twitter_profile(is_online, location):
    """
    Parameters
    ----------
    is_online : boolean
    location : str
        String to be set as user's location with no formatting.
        This function is not responsible for masking private location or offline status.
    """
    twitter = OAuth1Session(os.environ['twitter_consumer_key'],
                            os.environ['twitter_consumer_secret'],
                            os.environ['twitter_oauth_token'],
                            os.environ['twitter_oauth_token_secret'])
    params = {
        'name':
        name['name_template'].format(
            status=name[('on' if is_online else 'off') + 'line_status']),
        'location':
        location
    }
    twitter.post(
        'https://api.twitter.com/1.1/account/update_profile.json',
        params=params)
    return "lambda test"


def get_vrchat_status():
    if 'user_id' not in globals():
        logger.info("Fetching user_id")
        store_user_id_to_global()
    else:
        logger.info("Using cache: user_id")
    if 'api' not in globals():
        logger.info("Authenticating")
        store_api_session_to_global()
    else:
        logger.info("Using cache: api")
    logger.info("Fetching user info")
    info = fetch_user_info()  # Can't skip this line
    if info.status == Status.OFFLINE or info.location.offline:
        return False, offline_location
    if info.location.private or 'private' in info.location.instanceId:
        return True, private_location
    if 'previous_world_id' not in globals():
        logger.info("Fetching world info")
        store_world_info_to_global(info.location.worldId)
    elif previous_world_id != info.location.worldId:
        logger.info("Fetching world info")
        store_world_info_to_global(info.location.worldId)
    else:
        logger.info("Using cache: world_name")
    return True, world_name


def store_user_id_to_global():
    res = requests.get(
        'https://api.vrchat.cloud/api/1/auth/user?apiKey={}'.format(apiKey),
        auth=requests.auth.HTTPBasicAuth(os.environ['vrchat_username'],
                                         os.environ['vrchat_password']))
    logger.info('Response from VRChat: {}'.format(str(res)))
    global user_id
    user_id = res.json()['id']


def store_api_session_to_global():
    global api
    api = VRChatAPI(os.environ['vrchat_username'],
                    os.environ['vrchat_password'])
    api.authenticate(
    )  # Can be faster if modified as this endpoint is called twice


def fetch_user_info(is_retry=False):
    try:
        info = api.getUserById(user_id)
    except:
        if not is_retry:
            info = fetch_user_info(is_retry=True)
            logger.warning('User info fetch failed. Retrying...')
        logger.error('Cannot retrieve user info. Aborting!')
        raise
    return info


def store_world_info_to_global(world_id):
    global previous_world_id
    previous_world_id = world_id
    global world_name
    world_name = api.getWorldById(world_id).name