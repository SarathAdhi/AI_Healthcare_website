from distutils.log import debug
from flask import Flask, render_template, request, jsonify
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

app = Flask(__name__)

user_message = []
bot_message = []
link = []

def chatBot(msg):
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)

    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()


    # sentence = "do you use credit cards?"
    sentence = msg

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                arr = []
                
                arr.append(random.choice(intent['responses']))
                arr.append(intent['link'])
                return arr
    else:
        return("I do not understand...")


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
    return render_template("chatbot.html")

@app.route('/chatbot',methods = ['POST'])
def chatbotPost():
    if request.method == 'POST':
        msg = request.form['msg']
        user_message.append(msg)
        bot = chatBot(msg)
        bot_message.append(bot[0])
        link.append(bot[1])
        return render_template('chatbot.html', message = zip(user_message, bot_message, link) )

if __name__ == "__main__":
    app.run(debug=True)