import os
import requests
from requests_oauthlib import OAuth1Session
from vrchat_api import VRChatAPI
import logging
logger = logging.getLogger()

apiKey='JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26'
offline_location = 'リアルワールド出張中'
private_location = "(private in VRC)"
name = {
    'name_template': '柊 釘葉{status}',
    'online_status': '✅',
    'offline_status': '📴'
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
        os.environ['consumer_key'],
        os.environ['consumer_secret'],
        os.environ['oauth_token'],
        os.environ['oauth_token_secret']
    )
    params = {
        'name': name['name_template'].format(status = name[('on' if is_online else 'off') + 'line_status']),
        'location': location
    }
    twitter.post('https://api.twitter.com/1.1/account/update_profile.json', params=params)
    return "lambda test"

def get_vrchat_status():
    res = requests.post(
        'https://api.vrchat.cloud/api/1/auth/user?apiKey={}'.format(apiKey),
        auth=requests.auth.HTTPBasicAuth(os.environ['vrchat_username'], os.environ['vrchat_password'])
    ).json
    api = VRChatAPI(os.environ['vrchat_username'], os.environ['vrchat_password'])
    api.authenticate() # Can be faster if modified as this endpoint is called twice
    info = api.getUserById(res.id)
    if info.status == VRChatAPI.Status.OFFLINE:
        return False, offline_location
    location = info.location
    if location.private:
        return True, private_location
    return True, api.getWorldById(location.worldId).name
