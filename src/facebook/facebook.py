import sys
import facebookMessages as fb

# '''------------------------------------------------------------------------'''

def get_webhook(data):
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    if "text" in messaging_event["message"]:
                        if "quick_reply" in messaging_event["message"]:
                            quick_reply_postback = messaging_event["message"]["quick_reply"]["payload"]
                            handleQuickReplies(sender_id, quick_reply_postback)
                        else:
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
                        sender_id = messaging_event["sender"]["id"]
                        postback_payload = messaging_event["postback"]["payload"]
                        handlePostback(sender_id, postback_payload)

                    if messaging_event.get("delivery"):
                        pass

                    if messaging_event.get("optin"):
                        pass


# '''------------------------------------------------------------------------'''


def handlePostback(sender_id, postback_payload):
    if postback_payload == "GET_STARTED_BUTTON":
        sayHi(sender_id)

# '''------------------------------------------------------------------------'''


def sayHi(sender_id):
    user_name = fb.getUserData(sender_id)
    fb.send_message(sender_id, "Hi " + user_name + " " + u"\U0001F604")

# '''------------------------------------------------------------------------'''


def handleQuickReplies(sender_id, quick_reply_postback):
    pass


def handleMessage(sender_id, message_text):
    fb.send_message(sender_id, message_text)


def handleLocation(sender_id, user_lat_lon):
    pass


def handleSticker(sender_id, sticker_id):
    pass

def log(message):
    print str(message)
    sys.stdout.flush()
