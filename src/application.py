from facebook import facebook
from telefonica.telefonica_starting_conversation import BasicIntroduction
from flask import Flask
from flask import request
import os
from thread import start_new_thread
import thread

FACEBOOK_VERIFY_TOKEN = os.environ.get('FACEBOOK_VERIFY_TOKEN')


def hello():
    return 'hello'

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route('/telefonica-id', methods=['POST'])
def set_telefonica_id():
    print 'set telefonia id'
    data = request.get_json()
    print 'datta: ' + data
    BasicIntroduction.telefonica_id = data['id']
    return "ok", 200


@application.route('/facebook', methods=['GET'])
def verify():
    '''
     when the endpoint is registered as a webhook, it must echo back the
    'hub.challenge' value it receives in the query arguments
    '''
    if request.args.get("hub.mode") == "subscribe" \
            and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == FACEBOOK_VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@application.route('/facebook', methods=['POST'])
def webhook():
    print "got some stuff @ weebhook"
    '''
    endpoint for processing incoming messaging events
    '''
    data = request.get_json()
    start_new_thread(facebook.get_webhook, (data, ))
    print data
    return "ok", 200

# add rules
application.add_url_rule('/', 'index', hello)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
