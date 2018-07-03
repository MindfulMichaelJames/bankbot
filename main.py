# Python libraries that we need to import for our bot
import json
import random
import requests
import watson_developer_cloud
from flask import Flask, request
from googletrans import Translator
from pymessenger.bot import Bot
import bank_api


app = Flask(__name__)
ACCESS_TOKEN = 'EAAD6V6iE3WgBABDSCRcoGaF30IjKQwuzVZCzKV2WEstEedORTq28af8Xn1G3Fj7qLTm3ZAaWMUcMmX814nxDhILB83tbU8QUx16dKt4yyhpCJvh83Rd9TvMs6ZAfySSRWnraOSZCP0uubFGriRZBdMmqnrmEWRXCwgVCfSXvm2AZDZD'
VERIFY_TOKEN = 'BANKBOTTESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)
assistant = watson_developer_cloud.AssistantV1(
    username='be96309c-202b-46bd-b4c2-8208cea8f234',
    password='iUSjVYO5fLjb',
    version='2018-02-16'
)
translator = Translator()
account = {'balance': 120000,
           'beneficiaries': ["Ayanda Mhlongo", "Busi Dlamini"],
           'transactions': ["R200 to Jonas Mthembu", "R140 to Menzi Ndlovu"],
           'orders': ["Planet Fitness: R400", "Telkom: R700"]}


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
                    if message['message'].get('text'):
                        # Get FB message text in Zulu
                        zulu_response = message['message'].get('text')
                        # Translate FB message to English
                        english_response = zulu_to_english(zulu_response)
                        # Get intent from Watson
                        whole_response = get_response(english_response)
                        intent = whole_response['output']['text'][0]
                        # Get result of bank operation
                        english_result = bank_api.process_request(intent, account)
                        # Translate bank operation result to Zulu
                        zulu_result = english_to_zulu(english_result)
                        # Send Zulu result to FB message
                        send_message(recipient_id, zulu_result)
    return "Message processed"


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


@app.route('/connect')
def get_response(client_message):
    response = assistant.message(
        workspace_id='b5b8b4ce-af1f-49d4-8235-0229b7e01d57',
        input={
            'text': client_message
        }
    )
    return response


def english_to_zulu(etext):
    result = translator.translate(etext, src='en', dest='zu')
    # translate_client = translate.Client()
    # result = translate_client.translate(
    #     etext,
    #     target_language="Zulu")
    # return result["translatedText"]
    return result.text


def zulu_to_english(ztext):
    result = translator.translate(ztext, src='zu', dest='en')
    # translate_client = translate.Client()
    # result = translate_client.translate(
    #     ztext,
    #     target_language="English")
    # return result["translatedText"]
    return result.text


# uses PyMessenger to send response to user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    # return "success"


if __name__ == "__main__":
    app.run()