"""
Чат-бот 'ПРОГНОЗ ПОГОДЫ '
RastsislauFirstBot
"""
import requests
import json
from telebot import types
import secret

bot = secret.bot
API = secret.API

global city, data
count = 0
request_list = []


def count_message(message):
    global count
    count += 1
    if count < 11:
        request_list.append(message)
    else:
        request_list.append(message)
        request_list.pop(0)
    return request_list


@bot.message_handler(commands=['start'])
def start(message):
    mess = (f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!"
            f"\nЯ твой виртуальный помощник по погоде в любом городе мира.\n"
            f"Поздоровайся со мной (/hello_world или Привет)")
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['hello_world'])
def hello(message):
    bot.send_message(message.chat.id, f"И тебе еще раз <b>ПРИВЕТ</b>", parse_mode='html')
    bot.send_message(message.chat.id, f"\n Введи название города: ", parse_mode='html')
    bot.register_next_step_handler(message, get_weather )


@bot.message_handler(commands=['menu'])
def keys_button(message):
    bot.send_message(message.chat.id, f'<u>КНОПКИ:</u>'
                                      '\n<b>actual</b> - температура на данный момент'
                                      '\n<b>low</b> - минимальная температура за сутки'
                                      '\n<b>high</b> - максимальная температура за сутки'
                                      '\n<b>history</b> - история запросов', parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    low = types.KeyboardButton('/low')
    high = types.KeyboardButton('/high')
    actual = types.KeyboardButton('/actual')
    hist = types.KeyboardButton('/history')
    markup.add( actual, low, high, hist)
    bot.send_message(message.chat.id, 'Выбери команду:', reply_markup=markup)


@bot.message_handler(commands=['high'])
def high_temperature(message):
    global count
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, f'<b>{city}</b>: максимальная температура '
                                      f'за сутки: {data["main"]["temp_max"]} градуса', parse_mode='html')
    max_temp_message = f'{city}: максимальная температура за сутки: {data["main"]["temp_max"]} градуса'
    count_message(max_temp_message)
    bot.send_message(message.chat.id, 'Выбери следующую команду из меню или '
                                      'введи название нового города', reply_markup=markup)


@bot.message_handler(commands=['low'])
def low_temperature(message):
    global count
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, f'<b>{city}</b>: минимальная температура '
                                      f'за сутки: {data["main"]["temp_min"]} градуса', parse_mode='html')
    min_temp_message = f'{city}: минимальная температура за сутки: {data["main"]["temp_min"]} градуса'
    count_message(min_temp_message)
    bot.send_message(message.chat.id, 'Выбери следующую команду из меню или '
                                      'введи название нового города', reply_markup=markup)


@bot.message_handler(commands=['actual'])
def temperature_now(message):
    global count
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, f'<b>{city}</b>: температура на данный'
                                      f' момент: {data["main"]["temp"]} градуса', parse_mode='html')
    temp_message = f'{city}: температура на данный момент: {data["main"]["temp"]} градуса'
    count_message(temp_message)
    bot.send_message(message.chat.id, 'Выбери следующую команду из меню или '
                                      'введи название нового города', reply_markup=markup)


@bot.message_handler(commands=['history'])
def history(message):
    global request_list
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, f'<u>История последних 10 запросов: </u>', parse_mode='html')
    for elem in request_list:
        bot.send_message(message.chat.id, elem)
    bot.send_message(message.chat.id, 'Выбери следующую команду из меню или '
                                      'введи название нового города', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_weather(message):
    global city, data

    try:
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id, f"И тебе еще раз <b>ПРИВЕТ</b>", parse_mode='html')
            bot.send_message(message.chat.id, f"\n Введи название города: ", parse_mode='html')
            bot.register_next_step_handler(message, get_weather)
        else:
            city = message.text.strip().lower().title()
            res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
            data = json.loads(res.text)
            bot.send_message(message.chat.id, f'<b>страна: {data["sys"]["country"]}</b>\n', parse_mode='html')
            bot.register_next_step_handler(message, keys_button)
            bot.send_message(message.chat.id, 'Введи команду /menu: ')
    except KeyError:
        bot.reply_to(message, 'Такого города не существует. Введи верное название: ')
        bot.register_next_step_handler(message, get_weather)


bot.polling(none_stop=True)



#**********************************************************************************************
# import telebot
# import requests
# import json
# from telebot import types
#
# bot = telebot.TeleBot('6913680192:AAFXyv8wiuFcZkg5R1AKLXurmU-vQjmPuHA')
# API = '82f9ca8a481d778dd8030e5592633d8c'
#
# global city, data
# count = 0
# request_list = []
#
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     mess = (f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!"
#             f"\nЯ твой виртуальный помощник по погоде в любом городе мира.\n"
#             f"Поздоровайся со мной (/hello_world или Привет)")
#     bot.send_message(message.chat.id, mess, parse_mode='html')
#
#
# @bot.message_handler(commands=['hello_world'])
# def hello(message):
#     bot.send_message(message.chat.id, f"И тебе еще раз <b>ПРИВЕТ</b>", parse_mode='html')
#     bot.send_message(message.chat.id, f"\n Введи название города: ", parse_mode='html')
#     bot.register_next_step_handler(message, get_weather )
#
#
# @bot.message_handler(commands=['menu'])
# def keys_button(message):
#     bot.send_message(message.chat.id, f'<u>КНОПКИ:</u>'
#                                       '\n<b>custom</b> - температура на данный момент'
#                                       '\n<b>low</b> - минимальная температура за сутки'
#                                       '\n<b>high</b> - максимальная температура за сутки'
#                                       '\n<b>history</b> - история запросов', parse_mode='html')
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
#     low = types.KeyboardButton('/low')
#     high = types.KeyboardButton('/high')
#     custom = types.KeyboardButton('/custom')
#     history = types.KeyboardButton('/history')
#     markup.add( custom, low, high, history)
#     bot.send_message(message.chat.id, 'Выбери команду:', reply_markup=markup)
#
#
# @bot.message_handler(commands=['high'])
# def high_temperature(message):
#     global count
#     markup = types.InlineKeyboardMarkup()
#     bot.send_message(message.chat.id, f'<b>{city}</b>: максимальная температура '
#                                       f'за сутки: {data["main"]["temp_max"]} градуса', parse_mode='html')
#     max_temp_message = f'{city}: максимальная температура за сутки: {data["main"]["temp_max"]} градуса'
#     count += 1
#     if count < 11:
#         request_list.append(max_temp_message)
#     else:
#         request_list.append(max_temp_message)
#         request_list.pop(0)
#     bot.send_message(message.chat.id, 'Выбери следующую команду из меню или '
#                                       'введи название нового города', reply_markup=markup)
#
#
# @bot.message_handler(commands=['low'])
# def low_temperature(message):
#     global count
#     markup = types.InlineKeyboardMarkup()
#     bot.send_message(message.chat.id, f'<b>{city}</b>: минимальная температура '
#                                       f'за сутки: {data["main"]["temp_min"]} градуса', parse_mode='html')
#     min_temp_message = f'{city}: минимальная температура за сутки: {data["main"]["temp_min"]} градуса'
#     count += 1
#     if count < 11:
#         request_list.append(min_temp_message)
#     else:
#         request_list.append(min_temp_message)
#         request_list.pop(0)
#     bot.send_message(message.chat.id, 'Выбери следующую команду из меню или '
#                                       'введи название нового города', reply_markup=markup)
#
#
# @bot.message_handler(commands=['custom'])
# def temperature_now(message):
#     global count
#     markup = types.InlineKeyboardMarkup()
#     bot.send_message(message.chat.id, f'<b>{city}</b>: температура на данный'
#                                       f' момент: {data["main"]["temp"]} градуса', parse_mode='html')
#     temp_message = f'{city}: температура на данный момент: {data["main"]["temp"]} градуса'
#     count += 1
#     if count < 11:
#         request_list.append(temp_message)
#     else:
#         request_list.append(temp_message)
#         request_list.pop(0)
#     bot.send_message(message.chat.id, 'Выбери следующую команду из меню или '
#                                       'введи название нового города', reply_markup=markup)
#
#
# @bot.message_handler(commands=['history'])
# def history(message):
#     global request_list
#     markup = types.InlineKeyboardMarkup()
#     bot.send_message(message.chat.id, f'<u>История последних 10 запросов: </u>', parse_mode='html')
#     for elem in request_list:
#         bot.send_message(message.chat.id, elem)
#     bot.send_message(message.chat.id, 'Выбери следующую команду из меню или '
#                                       'введи название нового города', reply_markup=markup)
#
#
# @bot.message_handler(content_types=['text'])
# def get_weather(message):
#     global city, data
#
#     try:
#         if message.text.lower() == 'привет':
#             bot.send_message(message.chat.id, f"И тебе еще раз <b>ПРИВЕТ</b>", parse_mode='html')
#             bot.send_message(message.chat.id, f"\n Введи название города: ", parse_mode='html')
#             bot.register_next_step_handler(message, get_weather)
#         else:
#             city = message.text.strip().lower().title()
#             res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
#             data = json.loads(res.text)
#             bot.send_message(message.chat.id, f'<b>страна: {data["sys"]["country"]}</b>\n', parse_mode='html')
#             bot.register_next_step_handler(message, keys_button)
#             bot.send_message(message.chat.id, 'Введи команду /menu: ')
#     except KeyError:
#         bot.reply_to(message, 'Такого города не существует. Введи верное название: ')
#         bot.register_next_step_handler(message, get_weather)
#
#
# bot.polling(none_stop=True)