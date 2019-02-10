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
- offline_location
- private_location
- name_template
- online_status
- offline_status  
Other configurations like name template, status emoji are still hard-coded. These will be customizable via environment variables. I'll do it later, or it might be a good first issue.  

I know the following usage is too simplified and unkind. Maybe I will be writing more detailed one, or it might be a good first issue.

### Add yourself as your friend
You need to add yourself as your friend to use this tool. You cannot do that via VRChat web, but you can do it via VRChat API.
(I'm not sure if it is allowed, but there seems to be no problem in becoming a friend with oneself.)

### Setup
Upload zip file to AWS lambda with the runtime of python 3.7. Add a CloudWatch trigger of rate(2 minutes) or something like that.

## Estimated AWS costs
per month
* time per request: 2000 ms
* 1 month = 30 days
* rate = rate(2 minutes)
* log size per request: 1.04 kB
### lambda
2000 ms * 0.000000208 USD/100ms * 1 req/2min * (60*24*30) min/month = 0.089856 USD/month
### CloudWatch Event
1 USD/1,000,000events * 1 event/2min * (60*24*30) min/month = 0.0216 USD/month
### CloudWatch Log
0.50 USD/GB / (1024 MB/GB * 1024 KB/MB * (1024/1000) kB/KB) * 1.04kB/req. * 1 req./2min * (60*24*30) min/month = 0.0105 USD/month

**Total: 0.122 USD/month** (14.64 JPY/month (under 1 USD = 120 JPY))

## Links
The following links help the development of this repo.
- https://developer.twitter.com/en/docs/accounts-and-users/manage-account-settings/api-reference/post-account-update_profile
- https://vrchatapi.github.io/#/
- https://github.com/y23586/vrchat-api-python
