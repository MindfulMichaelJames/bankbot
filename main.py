# Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import requests
import json


app = Flask(__name__)
ACCESS_TOKEN = 'EAAD6V6iE3WgBABDSCRcoGaF30IjKQwuzVZCzKV2WEstEedORTq28af8Xn1G3Fj7qLTm3ZAaWMUcMmX814nxDhILB83tbU8QUx16dKt4yyhpCJvh83Rd9TvMs6ZAfySSRWnraOSZCP0uubFGriRZBdMmqnrmEWRXCwgVCfSXvm2AZDZD'
VERIFY_TOKEN = 'BANKBOTTESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    client_message = ""
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    send_message(recipient_id, "Received")
                    if message['message'].get('text'):
                        client_message = message['message'].get('text')
                        response = get_response(client_message)
                        send_message(recipient_id, response)
    return client_message


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


@app.route('/connect')
def get_response(query):
    api_url = 'https://dialogflow.googleapis.com/v2beta1/{session=projects/bankbot-868c9/agent/sessions/1234567890}:detectIntent?queryInput=' + query
    head = {'Authorization': 'Bearer 4414a0209d5f449d948420ee42f6aa9a'}
    s = requests.Session()
    result = s.get(api_url + query + '&lang=en', headers=head)
    # data = json.loads(result.text)
    return result.text


# uses PyMessenger to send response to user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run()
