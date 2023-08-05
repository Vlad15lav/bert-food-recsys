import io
import gdown
import telebot
import mysql.connector
import wget
import zipfile

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

def load_files():
    if not (os.path.exists(CONFIG["DATA_ITEMS"]) \
        and os.path.exists(CONFIG["TFIDF_ITEMS_PATH"]) \
        and os.path.exists(CONFIG["TFIDF_FEATURES"])):
            gdown.download("https://drive.google.com/uc?id=17nDmHE84dT76vsVrq-5RaqrEoJBdFMV7",
                "recsys_data.zip", quiet=False)
            
            with zipfile.ZipFile("recsys_data.zip", 'r') as zip_ref:
                zip_ref.extractall(".")
            
            os.remove("recsys_data.zip")
            wget.download("https://github.com/Vlad15lav/food-recsys/releases/download/v0.1.0/bert-food-cls.pth",
                out="weights/bert-food-cls.pth")

if __name__ == "__main__":
    create_tables(db_mysql)
    load_files()
    main()
    
