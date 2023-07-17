from telebot.types import ReplyKeyboardRemove
from database.queries import add_reviews

def feedback_handler(bot, message, db):
    empty_markup = ReplyKeyboardRemove()

    if message.text == "Впечатляет😋":
        add_reviews(db, message.from_user.id, 3)
        bot.send_message(message.chat.id, text="Спасибо за отзыв!", parse_mode='Markdown', reply_markup=empty_markup)
    elif message.text == "Нормально😐":
        add_reviews(db, message.from_user.id, 2)
        bot.send_message(message.chat.id, text="Спасибо за отзыв!", parse_mode='Markdown', reply_markup=empty_markup)
    elif message.text == "Не впечатляет😔":
        add_reviews(db, message.from_user.id, 1)
        bot.send_message(message.chat.id, text="Спасибо за отзыв!", parse_mode='Markdown', reply_markup=empty_markup)
    else:
        return False

    return True