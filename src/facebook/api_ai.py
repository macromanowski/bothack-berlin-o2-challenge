import os
import sys
import json
import requests
from flask import Flask, request
import apiai

#APIAI_CLIENT_ACCESS_TOKEN = os.environ.get('APIAI_CLIENT_ACCESS_TOKEN')
APIAI_CLIENT_ACCESS_TOKEN ='e394fa0f0f234e88837ae182e0a5eee5'
ai = apiai.ApiAI(APIAI_CLIENT_ACCESS_TOKEN)

def queryApiAi(text_to_NLP):
    apiai_request = ai.text_request()
    apiai_request.lang  = 'en'
    apiai_request.query = text_to_NLP
    response = apiai_request.getresponse()
    response = response.read()
    response = json.loads(response)
    if response["status"]["code"] != 200:
        print "API.AI error!"
        print "ERROR CODE: " + str(response["status"]["code"])
        print "ERROR TYPE: " + response["status"]["errorType"]
    else:
        return response

