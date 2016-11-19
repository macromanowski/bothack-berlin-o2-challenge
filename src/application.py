import os

from facebook import facebook
from flask import Flask
from flask import request


FACEBOOK_VERIFY_TOKEN = 'FB_VERIFY_TOKEN'


def hello():
    return 'hello'

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route('/facebook', methods=['GET'])
def verify():
    '''
     when the endpoint is registered as a webhook, it must echo back the
    'hub.challenge' value it receives in the query arguments
    '''
    if request.args.get("hub.mode") == "subscribe" \
            and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ[FACEBOOK_VERIFY_TOKEN]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@application.route('/facebook', methods=['POST'])
def webhook():
    '''
    endpoint for processing incoming messaging events
    '''
    data = request.get_json()
    facebook.get_webhook(data)
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
