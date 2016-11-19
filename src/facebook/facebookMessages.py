import sys
import json
import requests
import os

FACEBOOK_PAGE_ACCESS_TOKEN = 'FB_PAGE_ACCESS_TOKEN'


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    send_raw(data)

# '''------------------------------------------------------------------------'''


def send_raw(data):
    params = {
        "access_token": os.environ[FACEBOOK_PAGE_ACCESS_TOKEN]
    }
    headers = {
        "Content-Type": "application/json"
    }
    # SEND API REFERENCE
    # https://developers.facebook.com/docs/messenger-platform/send-api-reference
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    # log("SENT RAW! ")
    if r.status_code != 200:
        log('FB failed to response!')
        log('Response code: ' + r.status_code + ' with message: ' + r.text)

# '''------------------------------------------------------------------------'''


def getUserData(user_id):
    '''
    curl -X GET "https://graph.facebook.com/v2.6/<USER_ID>?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=PAGE_ACCESS_TOKEN"
    https://developers.facebook.com/docs/messenger-platform/user-profile
    '''

    url = "https://graph.facebook.com/v2.6/" + user_id + "?access_token=" + os.environ[FACEBOOK_PAGE_ACCESS_TOKEN]
    r = requests.get(url)

    user_data = r.text
    user_data = json.loads(user_data)
    first_name = user_data["first_name"]
    last_name = user_data["last_name"]
    profile_pic = user_data["profile_pic"]
    locale = user_data["locale"]
    timezone = user_data["timezone"]
    gender = user_data["gender"]

    '''TODO: add to DB'''

    return first_name

# '''------------------------------------------------------------------------'''


def log(message):
    print str(message)
    sys.stdout.flush()
