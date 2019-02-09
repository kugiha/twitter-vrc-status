import os
import requests
from requests_oauthlib import OAuth1Session
from vrchat_api import VRChatAPI
from vrchat_api.enum import Status
import logging
logger = logging.getLogger()

apiKey='JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26'
offline_location = 'offline'
private_location = "(private in VRC)"
name = {
    'name_template': '柊 釘葉 / Hiiragi Kugiha{status}',
    'online_status': '✅',
    'offline_status': '💤'
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
    twitter = OAuth1Session(
        os.environ['twitter_consumer_key'],
        os.environ['twitter_consumer_secret'],
        os.environ['twitter_oauth_token'],
        os.environ['twitter_oauth_token_secret']
    )
    params = {
        'name': name['name_template'].format(status = name[('on' if is_online else 'off') + 'line_status']),
        'location': location
    }
    twitter.post('https://api.twitter.com/1.1/account/update_profile.json', params=params)
    return "lambda test"

def get_vrchat_status():
    res = requests.get(
        'https://api.vrchat.cloud/api/1/auth/user?apiKey={}'.format(apiKey),
        auth=requests.auth.HTTPBasicAuth(os.environ['vrchat_username'], os.environ['vrchat_password'])
    )
    logger.info('Response from VRChat: {}'.format(str(res)))
    user_id = res.json()['id']
    api = VRChatAPI(os.environ['vrchat_username'], os.environ['vrchat_password'])
    api.authenticate() # Can be faster if modified as this endpoint is called twice
    info = api.getUserById(user_id)
    if info.status == Status.OFFLINE or info.location.offline:
        return False, offline_location
    if info.location.private:
        return True, private_location
    return True, api.getWorldById(info.location.worldId).name
