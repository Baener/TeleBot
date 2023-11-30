import pandas as pd #pip install pandas
from sklearn.linear_model import LinearRegression #pip install -U scikit-learn
from sklearn.model_selection import train_test_split 
import numpy as np

import telebot #pip install pyTelegramBotAPI
from telebot import types

token = "6548216408:AAEGA2EPniquuz2X4Eq9se15cU3L_IFJMP0"

predict = 0

rangeArea = [[23, 27],[28, 42],[50, 75],[70, 90]]

flats = ["студии", "1-комнатной квартиры", "2-комнатной квартиры", "3-комнатной квартиры"]

bot = telebot.TeleBot(token)

chatId = None

def GetPredict():
    data = pd.read_csv("dataset.csv", sep=';')
    data = data[::-1]
    projection = 1
    data['Прогноз'] = data['Стоимость'].shift(-projection)
    x = data[['Стоимость']][:-projection]
    y = data['Прогноз'][:-projection]
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state = 42)
    model = LinearRegression()
    model.fit(x_train, y_train)
    model.score(x_test, y_test)
    global predict
    predict = float(model.predict(data[['Стоимость']][-projection:])[0])

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}")
    global chatId
    chatId = message.chat.id
    GetPredict()
    markup = types.InlineKeyboardMarkup()
    btnBegin = types.InlineKeyboardButton("Начать", callback_data = 'begin')
    markup.add(btnBegin)
    bot.send_message(chatId, f"Начнем?", reply_markup=markup)

@bot.message_handler(commands=["begin"])
def begin(message):
    markup = types.InlineKeyboardMarkup()
    btn0 = types.InlineKeyboardButton("Студия", callback_data = '0')
    btn1 = types.InlineKeyboardButton("1-комнатная", callback_data = '1')
    btn2 = types.InlineKeyboardButton("2-комнатная", callback_data = '2')
    btn3 = types.InlineKeyboardButton("3-комнатная", callback_data = '3')
    markup.row(btn0, btn1)
    markup.row(btn2, btn3)
    bot.send_message(chatId, "Выберите количество комнат", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def sendResult(callback):
    if(callback.data != "begin"):
        pass
        bot.send_message(chatId, f"Для {flats[int(callback.data)]}")
        bot.send_message(chatId, "Прогноз на 14 дней:")
        bot.send_message(chatId, f"От {int(predict * rangeArea[int(callback.data)][0])} рублей")
        bot.send_message(chatId, f"До {int(predict * rangeArea[int(callback.data)][1])} рублей")
        markup = types.InlineKeyboardMarkup()
        btnBegin = types.InlineKeyboardButton("Да", callback_data = 'begin')
        markup.add(btnBegin)
        bot.send_message(chatId, f"Еще раз?", reply_markup=markup)
    else:
        begin(chatId)

bot.polling(none_stop=True)




    
