import os
import sys
import json
import requests
import time

FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')
print FACEBOOK_PAGE_ACCESS_TOKEN

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
        "access_token": FACEBOOK_PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    # SEND API REFERENCE
    # https://developers.facebook.com/docs/messenger-platform/send-api-reference
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    print r.text
    # log("SENT RAW! ")
    if r.status_code != 200:
        log('FB failed to response!')
        log('Response code: ' + str(r.status_code) + ' with message: ' + r.text)

# '''------------------------------------------------------------------------'''

def sendCallButton(sender_id):
    data = json.dumps({
          "recipient":{
            "id":sender_id
          },
          "message":{
            "attachment":{
              "type":"template",
                 "payload":{
                    "template_type":"button",
                    "text":"If you would like to talk to someone of your species, please contact our customer service :) ",
                    "buttons":[
                       {
                          "type":"phone_number",
                          "title":"Call o2",
                          "payload":"+4989787979444" 
                       }
                    ]
                 }
            }
        }
    })
    send_raw(data)



def sendImage(recipient_id, image_url):

    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
                "type":"image",
                "payload":{
                    "url":image_url,
                    "is_reusable":"true"
                }
            }
        }
    })
    send_raw(data)


def getUserData(user_id):
    '''curl -X GET "https://graph.facebook.com/v2.6/<USER_ID>?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=PAGE_ACCESS_TOKEN"
    https://developers.facebook.com/docs/messenger-platform/user-profile'''

    url = "https://graph.facebook.com/v2.6/" + user_id + "?access_token=" + FACEBOOK_PAGE_ACCESS_TOKEN
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

def sendWelcomeQuickReplies(recipient_id):
    data = json.dumps({
        "recipient": {
        "id": recipient_id
        },
        "message":{
        "text":"I am O2 BOT and I will help you today :) Before we start, let me know if you are an existing customer or are you just interested in products and services O2 offers?",
        "quick_replies":[
          {
            "content_type":"text",
            "title":"Existing customer",
            "payload":"EXISTING_CUSTOMER"
          },
          {
            "content_type":"text",
            "title":"New customer",
            "payload":"NEW_CUSTOMER"
          }
        ]
      }
    })
    send_raw(data)

# '''------------------------------------------------------------------------'''

def sendButtonsNewCustomer(sender_id):
    data = json.dumps({
        "recipient": {
        "id": sender_id
        },
        "message":{
        "text":"Are you interested in a specific plan or need help on finding something new?",
        "quick_replies":[
            {
                "content_type":"text",
                "title":"Inspire me",
                "payload":"START_QUESTIONS"
            },
            {
                "content_type": "text",
                "title": "I know, what I want",
                "payload": "SPECIFIC_PLAN"
            },
            {
                "content_type": "text",
                "title": "That's all, thanks!",
                "payload": "BYE_BYE"
            }
        ]
      }
    })
    send_raw(data)

# '''------------------------------------------------------------------------'''

def specific_plan_selection(sender_id):
    data = json.dumps(
        {
            "recipient": {
                "id": sender_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "o2 Plans",
                                "item_url": "https://www.o2online.de/tarife/",
                                "image_url": "https://www.telefonica.de/file/public/458/logo_o2_1_156x104.jpg",
                                "subtitle": "All plans provided by o2",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "https://www.o2online.de/tarife/",
                                        "title": "Show me o2 plans",
                                        "webview_height_ratio": "tall"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    )
    send_raw(data)


def send_minutes_question(sender_id):
    data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "Are you going to make calls mainly within O2 carrier or outside?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Inbound",
                    "payload": "SECOND_QUESTION"
                },
                {
                    "content_type": "text",
                    "title": "Outboud",
                    "payload": "SECOND_QUESTION"
                }
            ]
        }
    })
    send_raw(data)


def send_data_question(sender_id):
    data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "How many gigabytes of data will you need?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "0 GB",
                    "payload": "THIRD_QUESTION"
                },
                {
                    "content_type": "text",
                    "title": "5 GB",
                    "payload": "THIRD_QUESTION"
                },
                {
                    "content_type": "text",
                    "title": "10 GB",
                    "payload": "THIRD_QUESTION"
                }
            ]
        }
    })
    send_raw(data)


def send_price_question(sender_id):
    data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "How much do you wish to pay monthly?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Nothing ;)",
                    "payload": "SELECT_PLAN"
                },
                {
                    "content_type": "text",
                    "title": "10-20 EUR",
                    "payload": "SELECT_PLAN"
                },
                {
                    "content_type": "text",
                    "title": "It doesn't matter!",
                    "payload": "SELECT_PLAN"
                }
            ]
        }
    })
    send_raw(data)

def sendButtonsExistingCustomer(sender_id):
    data = json.dumps({
        "recipient": {
        "id": sender_id
        },
        "message":{
        "text":"I am O2 BOT and I will help you today :) Before we start, let me know if you are an existing customer or are you just interested in products and services O2 offers?",
        "quick_replies":[
          {
            "content_type":"text",
            "title":"Existing customer",
            "payload":"EXISTING_CUSTOMER"
          },
          {
            "content_type":"text",
            "title":"New customer",
            "payload":"NEW_CUSTOMER"
          }
        ]
      }
    })
    send_raw(data)

# '''------------------------------------------------------------------------'''

def sendNotificationDataWarning(user_id):
    first_name = getUserData(user_id)
    data = json.dumps({
        "recipient": {
        "id": user_id
        },
        "message":{
        "text":"Hey " +first_name+ ", you've used 80%% of your data this month and have 5 days left. How much data would you like to purchase? ",
        "quick_replies":[
          {
            "content_type":"text",
            "title":"500MB for 5 EUR",
            "payload":"POSTBACK_ADDATA_500MB"
          },
          {
            "content_type":"text",
            "title":"1GB for 10 EUR",
            "payload":"POSTBACK_ADDATA_1GB"
          },
          {
            "content_type":"text",
            "title":"No, thank you",
            "payload":"POSTBACK_ADDATA_NVM"
          }
        ]
      }
    })
    send_raw(data)

def sendNotificationAbnormal(user_id):
    first_name = getUserData(user_id)
    data = json.dumps({
        "recipient": {
        "id": user_id
        },
        "message":{
        "text":"Hey " +first_name+ ", you're using more data then usual this month, what would you like to do? ",
        "quick_replies":[
          {
            "content_type":"text",
            "title":"Extend your data",
            "payload":"POSTBACK_CALL_SEND_INTERNET"
          },
          {
            "content_type":"text",
            "title":"Nothing, leave as is",
            "payload":"LEAVE_AS_IS"
          }
        ]
      }
    })
    send_raw(data)

def sendNotificationHappyBirthday(user_id):
    first_name = getUserData(user_id)
    send_message(user_id, "Happy Birthday, " + first_name + "!")
    
# '''------------------------------------------------------------------------'''

def sendCheckingAccout(user_id):
    user_name = getUserData(user_id)
    send_message(user_id, "Great, " +user_name+ "! Looking into your account...")

# '''------------------------------------------------------------------------'''

def notEnaughData(user_id):
    data = json.dumps({
        "recipient": {
        "id": user_id
        },
        "message":{
        "text":"It's middle of the month and your turbo highspeed intenet is almost used up. Is this an issue you are dealing with?" + u"\U0001F680",
        "quick_replies":[
          {
            "content_type":"text",
            "title":"Sure!",
            "payload":"POSTBACK_DATA_SURE"
          },
          {
            "content_type":"text",
            "title":"Nope",
            "payload":"POSTBACK_DATA_NOPE"
          }
        ]
      }
    })
    send_raw(data)

def billToHigh(user_id):
    data = json.dumps({
        "recipient": {
        "id": user_id
        },
        "message":{
        "text":"Your bill is higher than it should be. Is this an issue you are dealing with?" + u"\U0001F680",
        "quick_replies":[
          {
            "content_type":"text",
            "title":"Yep :(",
            "payload":"POSTBACK_BILL_YES"
          },
          {
            "content_type":"text",
            "title":"Nope",
            "payload":"POSTBACK_BILL_NO"
          }
        ]
      }
    })
    send_raw(data)

def UsedRoaming(user_id, minutes_above):
    send_message(user_id, "Looks like you've been making some calls while in Shanghai, which is why your bill is high. You talked there " + str(minutes_above) + " minutes. Let me see if I can do something for you.")
    time.sleep(1)
    data = json.dumps({
        "recipient": {
        "id": user_id
        },
        "message":{
        "text":"Do you want to get an international roaming flat for 20EUR?",
        "quick_replies":[
          {
            "content_type":"text",
            "title":"Sure!",
            "payload":"POSTBACK_ROAMING_YES"
          },
          {
            "content_type":"text",
            "title":"Nope",
            "payload":"POSTBACK_ROAMING_NO"
          }
        ]
      }
    })
    send_raw(data)


def tooMuchPorn(user_id):
    send_message(user_id, "Oh, oh, oh! Looks like you've been chatting to to some hotties last night! Well done! Well, you want to get dirty, you have to pay! Let's see, what we can do:")
    sendImage(user_id, "http://i.makeagif.com/media/11-20-2016/CvvCRB.gif")
    time.sleep(1)
    send_message(user_id, "OK, OK... ;)")
    data = json.dumps({
        "recipient":{
        "id":user_id
      },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text":"Let's see, what we can do...",
            "buttons":[
              {
                "type":"postback",
                "title":"Block this number!",
                "payload":"POSTBACK_PORN_YES"
              },
              {
                "type":"postback",
                "title":"It was worth it!",
                "payload":"POSTBACK_PORN_NO"
              }
            ]
          }
        }
      }
    })
    send_raw(data)

def sendInternetOptions(user_id):
    data = json.dumps({
        "recipient":{
        "id":user_id
      },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text":"Would you like to top-up your data?",
            "buttons":[
              {
                "type":"postback",
                "title":"500MB for 5EUR",
                "payload":"POSTBACK_ADDATA_500MB"
              },
              {
                "type":"postback",
                "title":"1GB for 10EUR",
                "payload":"POSTBACK_ADDATA_1GB"
                },
              {
                "type":"postback",
                "title":"No, thanks!",
                "payload":"POSTBACK_ADDATA_NVM"
               }

            ]
          }
        }
      }
    })
    send_raw(data)

def sendOtherOptions(sender_id):
    data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "I'm glad to hear that! Is there anything else I can do?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Of course!",
                    "payload": "MAIN_MENU"
                },
                {
                    "content_type": "text",
                    "title": "No, thanks!",
                    "payload": "BYE_BYE"
                }
            ]
        }
    })
    send_raw(data)


def default_options(sender_id, complain_title):
    data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "How can I help?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": complain_title,
                    "payload": "COMPLAIN_BTN"
                },
                {
                    "content_type": "text",
                    "title": "I'm done, thank you!",
                    "payload": "BYE_BYE"
                }
            ]
        }
    })
    send_raw(data)

def send_tariffe(sender_id):
    data = json.dumps(
        {
            "recipient": {
                "id": sender_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "o2 Free M",
                                "item_url": "https://www.o2online.de/e-shop/tarif/o2-free-m",
                                "image_url": "https://www.telefonica.de/file/public/458/logo_o2_1_156x104.jpg",
                                "subtitle": "29.99 EUR\month",
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "https://www.o2online.de/e-shop/tarif/o2-free-m",
                                        "title": "Check tariff details",
                                        "webview_height_ratio": "tall"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    )
    send_raw(data)


def loginMessage(sender_id):
    data = json.dumps({
        "recipient": {
        "id": sender_id
        },
        "message":{
        "text":"Click login :) ",
        "quick_replies":[
          {
            "content_type":"text",
            "title":"LOGIN",
            "payload":"POSTBACK_LOGIN"
          }
        ]
      }
    })
    send_raw(data)
   
    time.sleep(1)

    send_message(sender_id, "OK! You are logged in! :) ")

def log(message):
    print str(message)
    sys.stdout.flush()