import telebot
import requests
import sqlite3
import os.path
from pathlib import Path

bot = telebot.TeleBot("")

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    con = sqlite3.connect('.venv/db/realt.db')
    cursor = con.cursor()
    cursor.execute("SELECT url FROM offers")

    for i in range (1, 100):
        print(cursor.fetchone())
        print(i)
        try:
            bot.send_message(chat_id, cursor.fetchone())
        except:
            print(cursor.fetchone())


bot.polling(none_stop=True)