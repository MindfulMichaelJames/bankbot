# -*- coding: utf-8 -*-
# Python libraries that we need to import for our bot
# import dialogflow
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAD6V6iE3WgBACqrKihuiypnBySVfNGZCmjW6HEcZBaZBPouF6PPmVSD1dbfFAqYDCTJ3A2Gry084MLHXNWBZC0dwoOkEwSwYoO8sIPrQVBGC1xL2y1QW3w6zEr4QwYFAg9ZAer1XLimcLTxiPVGHlWUoQqBdl9Nd6loHBpBcgwZDZD'
VERIFY_TOKEN = 'BANKBOTTESTINGTOKEN'
bot = Bot(ACCESS_TOKEN)


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
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
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    # if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!",
                        "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)


# uses PyMessenger to send response to user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run()


# def detect_intent_texts(project_id, session_id, texts, language_code):
#     """Returns the result of detect intent with texts as inputs.
#
#     Using the same `session_id` between requests allows continuation
#     of the conversaion."""
#     session_client = dialogflow.SessionsClient()
#
#     session = session_client.session_path(project_id, session_id)
#     print('Session path: {}\n'.format(session))
#
#     for text in texts:
#         text_input = dialogflow.types.TextInput(
#             text=text, language_code=language_code)
#
#         query_input = dialogflow.types.QueryInput(text=text_input)
#
#         response = session_client.detect_intent(
#             session=session, query_input=query_input)
#
#         print('=' * 20)
#         print('Query text: {}'.format(response.query_result.query_text))
#         print('Detected intent: {} (confidence: {})\n'.format(
#             response.query_result.intent.display_name,
#             response.query_result.intent_detection_confidence))
#         print('Fulfillment text: {}\n'.format(
#             response.query_result.fulfillment_text))