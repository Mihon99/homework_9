import telebot
from telebot import types
import random

bot = telebot.TeleBot("5593727093:AAGaK9E7D8xzhPQMx7p84HqQUTH3c3vpNYU")
sweets = 2021
max_sweet = 28
a = 0
name1 = 'User'
name2 = "bot"
flag = name1

@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id,"/button")
    
@bot.message_handler(commands = ["button"])
def button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Узнать правила игры")
    but2 = types.KeyboardButton("Играть")
    but3 = types.KeyboardButton("Рестарт")
    markup.add(but1)
    markup.add(but2)
    markup.add(but3)
    bot.send_message(message.chat.id,"Выбери ниже",reply_markup=markup)

@bot.message_handler(content_types = "text")
def controller(message):
    global flag
    if message.text == "Узнать правила игры":
        bot.send_message(message.chat.id,"Создайте программу для игры с конфетами человек против человека.Условие задачи: На столе лежит 2021 конфета. Играют два игрока делая ход друг после друга. Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет. Все конфеты оппонента достаются сделавшему последний ход. Сколько конфет нужно взять первому игроку, чтобы забрать все конфеты у своего конкурента?")
    elif message.text == "Играть":
        bot.send_message(message.chat.id,"Давай начнем")
        first_turn = random.choice([name1, name2])
        flag = name1 if first_turn == name1 else name2
        bot.register_next_step_handler(message,play)
    elif message.text == "Рестарт":
        restart(message)

@bot.message_handler(content_types = ["text"])
def user_turn(message):
    global a, sweets, flag    
    a = int(message.text)
    turn = a
    sweets -= turn
    if sweets>0:
        bot.send_message(message.chat.id,f'Конфет осталось - {sweets}')
    else:
        bot.send_message(message.chat.id,f'Конфет осталось - 0')
    flag = name2 if flag == name1 else name1
    play(message)

@bot.message_handler(content_types = ["text"])
def bot_turn(message):
    global a, max_sweet, sweets, flag
    turn = random.randint(1,max_sweet+1)
    bot.send_message(message.chat.id,f"bot взял {turn} конфет. ")
    sweets -= turn
    if sweets == 0:
        bot.send_message(message.chat.id,f'Конфет осталось - 0')
    flag = name2 if flag == name1 else name1
    play(message)

def play(message):
    global a, sweets, max_sweet, flag
    if sweets>0:
        bot.send_message(message.chat.id,f"ходит {flag}, конфет осталось - {sweets}")
        if flag == name1:
                bot.send_message(message.chat.id,"Введите кол-во конфет от 1 до 28")
                bot.register_next_step_handler(message,user_turn)
        else:
                bot_turn(message)
    else:
        winner = name2 if flag == name1 else name1
        bot.send_message(message.chat.id,f"Поздравляем победил игрок {winner}")

def restart(message):
    global a, sweets, max_sweet, flag
    a = 0
    sweets = 2021
    max_sweet = 28
    flag = name1



bot.infinity_polling()