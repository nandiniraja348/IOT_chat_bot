from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
app = Flask(__name__)
iot_bot=ChatBot("IOT_Chat_Bot", storage_adapter="chatterbot.storage.SQLStorageAdapter",logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. Enter a valid question.',
            'maximum_similarity_threshold': 0.90
        }
    ])

trainer=ListTrainer(iot_bot)
trainer.train([
    "Hi",
    "Hi Dude!",
    "Hello",
    "Hello Dude!",
    "How are you?",
    "I am good.",
    "That is good to hear.",
    "Thank you",
    "You are welcome.",
     "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
])
for line in os.listdir('questions'):
    Bot_Info=open('questions/'+line,'r').readlines()
    trainer.train(Bot_Info)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/help")
def help():
    return render_template("question.html")
@app.route("/get")
def chatbotiot():
    userText = request.args.get('ques')
    print(userText)
    if(userText==''):
        decoded_string="Please ask a question."
    else:
        iot_bot_response=str(iot_bot.get_response(userText))
        decoded_string = bytes(iot_bot_response, "utf-8").decode("unicode_escape") 
    print(decoded_string)
    return str(decoded_string)


if __name__ == "__main__":
    app.run(debug=True)
