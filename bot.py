import io
import telebot
import mysql.connector

from handlers.start_handler import start_handler
from handlers.recommendation_handler import recommendation_handler
from handlers.feedback_handler import feedback_handler

from database.create_tables import create_tables 

from config import CONFIG

bot = telebot.TeleBot(CONFIG['TOKEN'])
db_mysql = mysql.connector.connect(**CONFIG['DATABASE'])


@bot.message_handler(commands=['start'])
def handle_start(message):
    if not db_mysql.is_connected():
        db_mysql.reconnect()

    start_handler(bot, message, db_mysql)


@bot.message_handler(content_types=['text'])
def handle_recomendation(message):
    if not db_mysql.is_connected():
        db_mysql.reconnect()
    
    if not feedback_handler(bot, message, db_mysql):
        recommendation_handler(bot, message, db_mysql)


def main():
    print("AI Chef бот запущен!")
    bot.polling(none_stop=True)


if __name__ == "__main__":
    create_tables(db_mysql)
    main()
    