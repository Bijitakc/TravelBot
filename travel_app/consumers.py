from channels.auth import channel_session_user_from_http,channel_session_user,channel_session

from channels import Channel
from channels.sessions import channel_session, enforce_ordering


from django.shortcuts import render

from travel_app.models import BotMessage,BotReply

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import pickle
import numpy as np
from keras.models import load_model
model = load_model('travel_app/models/chatbot_model.keras')

import json
import random

intents = json.loads(open('travel_app/models/intents.json').read())
words = pickle.load(open('travel_app/models/words.pkl','rb'))
classes = pickle.load(open('travel_app/models/classes.pkl','rb'))
  
@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})

@channel_session_user
def ws_disconnect(message):
    discard(message.reply_channel)

# This function will display all messages received in the console
@channel_session
def ws_recieve(message):
    print(message)
    botimp=message['text']

    print(botimp)
    ins=BotMessage(botinputs=botimp)
    ins.save()
   
    #message.reply_channel.send(json.loads(botimp))
    ints = predict_class(botimp, model)
    if len(ints) >= 1:
        res = getResponse(ints, intents)
    else:
        res=("Sorry I don't understand you. Can you repeat the question?")

    message.reply_channel.send({
        "text": res,
    })
    print(res) 
    

def clean_up_sentence(sentence):
        # tokenize the pattern - split words into array
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return(np.array(bag))

def predict_class(sentence, model):
        # filter out predictions below a threshold
        p = bow(sentence, words,show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.70
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        return return_list


def getResponse(ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result