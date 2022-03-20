from distutils.log import debug
from email import message
from flask import Flask, render_template, request, jsonify
import json
from chatbot import chatBot

app = Flask(__name__)

user_message = []
bot_message = []
link = []


@app.get("/")
def home():
    return render_template("index.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/API")
def API():
    f = open('database.json')
    data = json.load(f)
    return data

@app.get("/description")
def blog():
    return render_template("blog.html")

@app.get("/chatbot")
def chatbot():
    length = len(user_message)
    if length == 0:
        return render_template("chatbot.html")
    else:
        return render_template('chatbot.html', message = zip(user_message, bot_message, link))

@app.route('/chatbot',methods = ['POST'])
def chatbotPost():
    if request.method == 'POST':
        msg = request.form['msg']
        user_message.append(msg)
        bot = chatBot(msg)
        bot_message.append(bot[0])
        link.append(bot[1])
        return render_template('chatbot.html', message = zip(user_message, bot_message, link))

if __name__ == "__main__":
    app.run()