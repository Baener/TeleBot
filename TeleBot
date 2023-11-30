import pandas as pd #pip install pandas
from sklearn.linear_model import LinearRegression #pip install -U scikit-learn
from sklearn.model_selection import train_test_split 
import numpy as np

import telebot #pip install telebot
from telebot import types

token = "6548216408:AAEGA2EPniquuz2X4Eq9se15cU3L_IFJMP0"

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}")
    global chatId
    chatId = message.chat.id
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
    else:
        begin(chatId)

bot.polling(none_stop=True)
