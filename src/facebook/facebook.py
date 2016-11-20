import sys
import os
import facebookMessages as fb
from telefonica.telefonica_starting_conversation import BasicIntroduction
from telefonica.tariffe import TariffeDatabase
import random
import api_ai

FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')
user_data = None
is_complain_context = False

# '''------------------------------------------------------------------------'''

def get_webhook(data):
    global is_complain_context
    print "in get_webhook"
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    if is_complain_context and messaging_event["message"]["text"] == 'hi':
                        is_complain_context = False
                        fb.sendOtherOptions(sender_id)
                        return

                    if is_complain_context:
                        is_complain_context = False
                        fb.send_message(sender_id, "Thank you for your message. We will contact with you shortly! :)")
                        fb.send_message(sender_id, "And if you are satisfied with customer service, please like our fanpage! :)")
                        return
                    if "text" in messaging_event["message"]:
                        if "quick_reply" in messaging_event["message"]:
                            print "in quick reply"
                            quick_reply_postback = messaging_event["message"]["quick_reply"]["payload"]
                            handleQuickReplies(sender_id, quick_reply_postback)
                        else:
                            sender_id = messaging_event["sender"]["id"]
                            if is_complain_context and messaging_event["message"]["text"] == 'hi':
                                is_complain_context = False
                                fb.sendOtherOptions(sender_id)
                                return

                            if is_complain_context:
                                is_complain_context = False
                                fb.send_message(sender_id,
                                                "Thank you for your message. We will contact with you shortly! :)")
                                return
                            message_text = messaging_event["message"]["text"]
                            handleMessage(sender_id, message_text)
                    elif "attachments" in messaging_event["message"]:
                        if "coordinates" in messaging_event["message"]["attachments"][0]["payload"]:
                            user_lat_lon = [messaging_event["message"]["attachments"][0]["payload"]["coordinates"]["lat"], messaging_event["message"]["attachments"][0]["payload"]["coordinates"]["long"]]
                            handleLocation(sender_id, user_lat_lon)
                        elif "sticker_id" in messaging_event["message"]["attachments"][0]["payload"]:
                            sticker_id = messaging_event["message"]["attachments"][0]["payload"]["sticker_id"]
                            handleSticker(sender_id, sticker_id)
                        elif "image" in messaging_event["message"]["attachments"][0]["type"]:
                            fb.send_message(sender_id, "(y)")
                        elif "audio" in messaging_event["message"]["attachments"][0]["type"]:
                            fb.send_message(sender_id, "(y)")

                if messaging_event.get("postback"):
                    print "messaging event - postback"
                    sender_id = messaging_event["sender"]["id"]
                    postback_payload = messaging_event["postback"]["payload"]
                    handlePostback(sender_id, postback_payload)

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass


# '''------------------------------------------------------------------------'''


def handleQuickReplies(sender_id, postback_payload):
    print postback_payload
    global user_data
    global is_complain_context
    print postback_payload
    if postback_payload == "GET_STARTED_BUTTON":
        sayHi(sender_id)
    elif postback_payload == "NEW_CUSTOMER":
        fb.sendButtonsNewCustomer(sender_id)
    elif postback_payload == "EXISTING_CUSTOMER":
        print "enter existing"
        fb.loginMessage(sender_id)
        print "#2"
        user_data = BasicIntroduction(sender_id)
        print "#3"
        basic_info = user_data.get_basic_plan_information()
        fb.send_message(sender_id, "Your plan is: ")
        fb.send_tariffe(sender_id)
        if user_data.is_not_enough_data():
            fb.notEnaughData(sender_id)
        else:
            fb.billToHigh(sender_id)
    elif postback_payload == "POSTBACK_DATA_SURE":
        fb.sendInternetOptions(sender_id)
    elif postback_payload == "POSTBACK_DATA_NOPE":
        fb.sendOtherOptions(sender_id)   #TODO
    
    elif postback_payload == "POSTBACK_ROAMING_YES":
        fb.send_message(sender_id, "OK, jou just bought international roaming flat for 20EUR ")
        fb.sendOtherOptions(sender_id)
    elif postback_payload == "POSTBACK_ROAMING_NO":
        fb.sendOtherOptions(sender_id)
    elif postback_payload == "POSTBACK_BILL_YES":
        if bool(random.getrandbits(1)):
            minutes_above = 50
            if user_data is not None:
                minutes_above = user_data.minutes_above_plan()

            fb.UsedRoaming(sender_id, minutes_above)
        else:
            fb.tooMuchPorn(sender_id)

    elif postback_payload == "POSTBACK_BILL_NO":
        fb.sendOtherOptions(sender_id)

    elif postback_payload == "POSTBACK_CALL_SEND_INTERNET":
        fb.sendInternetOptions(sender_id)

    elif postback_payload == "LEAVE_AS_IS":
        fb.sendOtherOptions(sender_id)

    elif postback_payload == "POSTBACK_ADDATA_500MB":
        fb.send_message(sender_id, "OK, Done! You just bought 500MB package :) ")
        fb.sendOtherOptions(sender_id)
    elif postback_payload == "POSTBACK_ADDATA_1GB":
        fb.send_message(sender_id, "OK, Done! You just bought 1GB package :) ")
        fb.sendOtherOptions(sender_id)
    elif postback_payload == "POSTBACK_ADDATA_10GB":
        fb.send_message(sender_id, "OK, Done! You just bought 10GB package :) ")
        fb.sendOtherOptions(sender_id)
    elif postback_payload == "POSTBACK_ADDATA_NVM":
        fb.send_message(sender_id, "OK, never mind :P :) ")

    elif postback_payload == "MAIN_MENU":
        complain_button = "I am pissed of at my contract"
        if user_data is not None and user_data.get_user_age() < 25:
            complain_button = "You suck, I don't like you!"
        fb.default_options(sender_id, complain_button)
    elif postback_payload == "COMPLAIN_BTN":
        is_complain_context = True
        fb.send_message(sender_id, "Sorry to hear that! Please write us a message and a real human will get back to you.")

    elif postback_payload == "START_QUESTIONS":
        fb.send_minutes_question(sender_id)
    elif postback_payload == "SECOND_QUESTION":
        fb.send_data_question(sender_id)
    elif postback_payload == "THIRD_QUESTION":
        fb.send_price_question(sender_id)
    elif postback_payload == "SELECT_PLAN":
        fb.send_message(sender_id, "Here is our plan suited especially for you!")
        fb.send_tariffe(sender_id)
        fb.sendButtonsNewCustomer(sender_id)

    elif postback_payload == "SPECIFIC_PLAN":
        fb.specific_plan_selection(sender_id)
        fb.sendButtonsNewCustomer(sender_id)

    elif postback_payload == "BYE_BYE":
        fb.send_message(sender_id, "It was a pleasure talking to you! Hey, do you want to be friends on facebook?"
                                   " Like O2 and we will stay in touch")


# '''------------------------------------------------------------------------'''


def handlePostback(sender_id, postback_payload):
    print postback_payload
    if postback_payload == "POSTBACK_ADDATA_500MB":
        fb.send_message(sender_id, "OK, Done! You just bought 500MB package :) ")
        fb.sendOtherOptions(sender_id)
    elif postback_payload == "POSTBACK_ADDATA_1GB":
        fb.send_message(sender_id, "OK, Done! You just bought 1GB package :) ")
        fb.sendOtherOptions(sender_id)
    elif postback_payload == "POSTBACK_ADDATA_10GB":
        fb.send_message(sender_id, "OK, Done! You just bought 10GB package :) ")
        fb.sendOtherOptions(sender_id)
    elif postback_payload == "POSTBACK_ADDATA_NVM":
        fb.send_message(sender_id, "OK, never mind :P :) ")
        fb.sendOtherOptions(sender_id)
    elif postback_payload == "POSTBACK_PORN_YES":
        fb.send_message(sender_id, "We've blocked them for you! ;)")
        fb.sendOtherOptions(sender_id)

    elif postback_payload == "POSTBACK_PORN_NO":
        fb.send_message(sender_id, "Have fun! ;)")
        fb.sendOtherOptions(sender_id)

    elif postback_payload == "DATA_WARNING":
        fb.sendNotificationDataWarning(sender_id)

    elif postback_payload == "DATA_ABNORMAL":
        fb.sendNotificationAbnormal(sender_id)

    elif postback_payload == "HAPPY_BIRTHDAY":
        fb.sendNotificationHappyBirthday(sender_id)

    elif postback_payload == "HELP":
        fb.send_message(sender_id, "Hello, my name is O2Bot and I am an artificial intelligence. I can help you to solve some basic problems around your bill and contract with O2. If you are a wannabe customer, I can help you on that too.")
        fb.sendCallButton(sender_id)
    elif postback_payload == "START_OVER":
        sayHi(sender_id)

def handleMessage(sender_id, message_text):
    NLP_response = api_ai.queryApiAi(message_text)
    nlp_action = NLP_response["result"]["action"]

    if nlp_action == "greetings":
        #"Some of NLP contexts found"
        sayHi(sender_id)    
    elif nlp_action == "appraisal" or nlp_action == "cool" or nlp_action == "question_name" or nlp_action == "question_gender" or nlp_action == "smalltalk.agent" or nlp_action == "smalltalk.user":
        fb.send_message(sender_id, NLP_response["result"]["fulfillment"]["speech"])
    elif nlp_action == "fuck":
        fb.send_message(sender_id, NLP_response["result"]["fulfillment"]["speech"])
        fb.sendImage(sender_id, "http://gifyu.com/images/giphy1e4d5a.gif")
    elif nlp_action == "start":
        #"User wants to start over the conversation"
        sayHi(sender_id)
    elif nlp_action == "i_love_you":
        user_name = fb.getUserData(sender_id)
        fb.send_message(sender_id, user_name + " -> friendzone")
    elif nlp_action == "mobile_data":
        data_left = random.randint(1, 10)
        fb.send_message(sender_id, data_left + " GBs left :) ")
    elif nlp_action == "help":
        fb.send_message(sender_id, "Hello, my name is O2Bot and I am an artificial intelligence. I can help you to solve some basic problems around your bill and contract with O2. If you are a wannabe customer, I can help you on that too.")
        fb.sendCallButton(sender_id)
    elif message_text == ":)" or message_text == ":-)" or message_text == ":D" or message_text.encode('unicode-escape')[:-1] == "\\U0001f60" or message_text.encode('unicode-escape') == "\\U0001f642":
        fb.send_message(sender_id, u"\U0001F603")
    else:
        fb.sendImage(sender_id, "https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif")
        fb.send_message(sender_id, "Oops, I didn't catch that. For things I can help you with, type 'help'.")


def handleLocation(sender_id, user_lat_lon):
    fb.send_message(sender_id, "(y)")


def handleSticker(sender_id, sticker_id):
    if sticker_id == 144885035685763:
        fb.send_message(sender_id, "Meow! :)")
    else:
        fb.send_message(sender_id, "(y)")

# '''------------------------------------------------------------------------'''

def sayHi(sender_id):
    user_name = fb.getUserData(sender_id)
    fb.send_message(sender_id, "Hi " + user_name + "!")
    fb.sendWelcomeQuickReplies(sender_id)

# '''------------------------------------------------------------------------'''

def log(message):
    print str(message)
    sys.stdout.flush()
