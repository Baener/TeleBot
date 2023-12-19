import pandas as pd #pip install pandas
from sklearn.linear_model import GradientBoostingRegressor #pip install -U scikit-learn
from sklearn.model_selection import train_test_split 
import numpy as np

from datetime import datetime

import telebot #pip install pyTelegramBotAPI
from telebot import types

import parcer as pr

#pip install openpyxl Для чтения xlsx-файла

token = "6548216408:AAEGA2EPniquuz2X4Eq9se15cU3L_IFJMP0"

parc = []
predict = 0
count = 0

pars = []

flats = ["студии", "1-комнатной квартиры", "2-комнатной квартиры", "3-комнатной квартиры"]

bot = telebot.TeleBot(token)

chatId = None   

def GetPredict():
    global count
    if count == 0:
        global pars
        pars = pr.GetParcing()
        read_file = pd.read_excel ("data.xlsx")
        read_file.to_csv ("data.csv", index = None, header=True)
        data = pd.read_csv("data.csv", sep=',')
        data = data[[data.columns[0], data.columns[3]]]
        data.columns = ['Дата', 'Стоимость']
        for i in range(len(data) // 2):
            valueRow = data.at[i, data.columns[0]]
            valueCol = data.at[i, data.columns[1]]
            data.at[i, data.columns[0]] = data.at[len(data) - i - 1, data.columns[0]]
            data.at[i, data.columns[1]] = data.at[len(data) - i - 1, data.columns[1]]
            data.at[len(data) - i - 1, data.columns[0]] = valueRow
            data.at[len(data) - i - 1, data.columns[1]] = valueCol
        data.loc[len(data)] = [datetime.date, pars[4]]
        projection = 1
        data['Прогноз'] = data[data.columns[1]].shift(-projection)
        x = data[['Стоимость']][:-projection]
        y = data['Прогноз'][:-projection]
        x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state = 42)
        model = GradientBoostingRegressor()
        model.fit(x_train, y_train)
        model.score(x_test, y_test)
        global predict
        count += 1
        predict = float(model.predict(data[['Стоимость']][-projection:])[0])
    else:
        return

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, это Прогноз цен")
    bot.send_message(message.chat.id, f"С моей помощью ты можешь узнать прогноз стоимости квартиры в Ростове-на-Дону")
    global chatId
    chatId = message.chat.id
    GetPredict()
    markup = types.InlineKeyboardMarkup()
    btnBegin = types.InlineKeyboardButton("Начать", callback_data = 'begin')
    markup.add(btnBegin)
    bot.send_message(chatId, f"Начнем?", reply_markup=markup)

@bot.message_handler(commands=["begin"])
def begin(message):
    if predict == 0:
        start(message)
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
        bot.send_message(chatId, f"Для {flats[int(callback.data)]}")
        bot.send_message(chatId, "Прогноз на 14 дней:")
        bot.send_message(chatId, f"{int(predict * pars[int(callback.data)])} рублей")
        #bot.send_message(chatId, f"От {int(predict * rangeArea[int(callback.data)][0])} рублей")
        #bot.send_message(chatId, f"До {int(predict * rangeArea[int(callback.data)][1])} рублей")
        markup = types.InlineKeyboardMarkup()
        btnBegin = types.InlineKeyboardButton("Да", callback_data = 'begin')
        markup.add(btnBegin)
        bot.send_message(chatId, f"Еще раз?", reply_markup=markup)
    else:
        if chatId == None:
            start(callback.message)
            return
        begin(callback.message)

bot.polling(none_stop=True)




    
