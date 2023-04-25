import time

import telebot
from telebot import types

from config import *

bot = telebot.TeleBot(TOKEN)
all_users = dict()

def logging(func):
    def wrapper(*args, **kwargs):
        print(f"{args[1].from_user.username}({args[1].from_user.id}): {args[1].text}")
        func(*args, **kwargs)
    return wrapper

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.current_status = 'Off'
        self.msg = ''
    
    @logging
    def handler(self, message):
        if message.text == "/start":
            self.send("hello world")

    def query_handler(self, call):
        pass

    def send(self, msg, markup=None):
        return bot.send_message(self.user_id, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def query_handler(call):
    global all_users

    if not all_users.get(call.from_user.id):
        all_users[call.from_user.id] = User(call.from_user.id)

    all_users.get(call.from_user.id).query_handler(call)


@bot.message_handler(content_types=['text'])
def main(msg):
    global all_users

    if not all_users.get(msg.from_user.id):
        all_users[msg.from_user.id] = User(msg.from_user.id)

    all_users.get(msg.from_user.id).handler(msg)

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        time.sleep(5)
        print(e)
