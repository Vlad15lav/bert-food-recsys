import random

from telebot import types

from utils.loader import load_data, load_model_tfidf, load_model_bert
from models.recommendation_model import get_bert_recommendation, get_tfidf_recomendation

from database.queries import get_id_model, get_id_user, add_request

data_items, bert_embed_items, tfidf_embed_items = load_data()

tfidf_model = load_model_tfidf()
bert_model, tokenizer = load_model_bert()

MODELS_NUM = {
    1: "TF-IDF",
    2: "BERT"
}

def recommendation_handler(bot, message, db):
    """
    Создаем рекомендацию для пользователя
    """
    id_model = get_id_model(db, message.from_user.username)

    if id_model is None:
        id_model = int(random.random() < 0.5) + 1

    # Получаем рейтинг сходства рецептов
    if MODELS_NUM[id_model] == "TF-IDF":
        ranking = get_tfidf_recomendation(message.text, tfidf_model, tfidf_embed_items)
    else:
        ranking = get_bert_recommendation(message.text, tokenizer, bert_model, bert_embed_items)
    
    # Создаем текст рекомендации
    id_item = int(ranking[0])
    text_send = "Название: {}\nСостав: {}\n{}. Время готовки: {}".format(*data_items.loc[[id_item],
            ['name', 'ingredient', 'type_kitchen', 'time_cook']].values.reshape(-1))
    text_send += f"\n\nПодробнее рецепт по [ссылке]({data_items.loc[id_item, 'link']})"

    # Создаем UI кнопки бота для оценки рекомендации
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_eval_5 = types.KeyboardButton("Впечатляет😋")
    btn_eval_4 = types.KeyboardButton("Интересно🙂")
    btn_eval_3 = types.KeyboardButton("Стандартно😐")
    btn_eval_2 = types.KeyboardButton("Не уверен😕")
    btn_eval_1 = types.KeyboardButton("Не впечатляет😔")
    markup.add(btn_eval_5, btn_eval_4, btn_eval_3, btn_eval_2, btn_eval_1)

    # Отправляем рекомендацию
    bot.send_message(message.chat.id, text=text_send, parse_mode='Markdown', reply_markup=markup)
    if random.random() < 0.5:
        bot.send_message(message.chat.id, text="Оцените пожалуйста рекомендацию", parse_mode='Markdown', reply_markup=markup)

    # Сохраняем рекомендацию в базу данных
    id_user = get_id_user(db, message.from_user.username)
    add_request(db, id_user, id_item, id_model)