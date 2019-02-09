# twitter-vrc-status
Update your twitter location or name according to your VRC status

## Caution
This tool depends on the VRChat API, which is not officially supported, so this tool might suddenly stop working.  
Be advised that the **request rate over 1 req./min is prohibited**, and it can lead to undesirable consequences.  

## Usage
### Configurations
Set these environment variables  
- twitter_consumer_key
- twitter_consumer_secret
- twitter_oauth_token
- twitter_oauth_token_secret
- vrchat_username
- vrchat_password  
Other configurations like name template, status emoji are still hard-coded. These will be customizable via environment variables. I'll do it later, or it might be a good first issue.  

I know the following usage is too simplified and unkind. Maybe I will be writing more detailed one, or it might be a good first issue.

### Add yourself as your friend
You need to add yourself as your friend to use this tool. You cannot do that via VRChat web, but you can do it via VRChat API.
(I'm not sure if it is allowed, but there seems to be no problem in becoming a friend with oneself.)

### Setup
Upload zip file to AWS lambda with the runtime of python 3.7. Add a CloudWatch trigger of rate(2min) or something like that.

## Links
The following links help the development of this repo.
- https://developer.twitter.com/en/docs/accounts-and-users/manage-account-settings/api-reference/post-account-update_profile
- https://vrchatapi.github.io/#/
- https://github.com/y23586/vrchat-api-python
