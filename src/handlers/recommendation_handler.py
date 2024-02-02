import random

from telebot import types

from utils.loader import load_files, load_data, \
                        load_model_tfidf, load_model_bert

from models.recommendation_model import get_bert_recommendation, \
                                        get_tfidf_recomendation

from database.queries import get_model_id, get_user_id, add_request
from config import CONFIG


load_files()
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
    model_id = get_model_id(db, message.from_user.id)

    # Выбираем модель рекомендации для пользователя
    if CONFIG["A/B_STATUS"]:
        if model_id is None:
            model_id = random.randint(1, 2)
    else:
        if CONFIG["MODEL_SELECT"] == "TF-IDF":
            model_id = 1
        else:
            model_id = 2

    # Получаем рейтинг сходства рецептов
    if MODELS_NUM[model_id] == "TF-IDF":
        ranking = get_tfidf_recomendation(message.text,
                                          tfidf_model,
                                          tfidf_embed_items)
    else:
        ranking = get_bert_recommendation(message.text,
                                          tokenizer,
                                          bert_model,
                                          bert_embed_items)

    # Создаем текст рекомендации
    items_id = [int(ranking[i]) for i in range(3)]

    # Сохраняем рекомендацию в базу данных
    user_id = get_user_id(db, message.from_user.id)
    add_request(db, user_id, items_id, model_id)

    # Создаем UI кнопки бота для оценки рекомендации
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_eval_3 = types.KeyboardButton("Впечатляет😋")
    btn_eval_2 = types.KeyboardButton("Нормально😐")
    btn_eval_1 = types.KeyboardButton("Не впечатляет😔")
    markup.add(btn_eval_3, btn_eval_2, btn_eval_1)

    for item_id in items_id:
        text_send = "Название: {}\nСостав: {}\n{}. Время готовки: {}"\
                    .format(*data_items.loc[[item_id],
                                            ['name',
                                             'ingredient',
                                             'type_kitchen',
                                             'time_cook']].values.reshape(-1))

        text_send += "\n\nПодробнее рецепт по [ссылке]"\
            f"({data_items.loc[item_id, 'link']})"

        # Отправляем рекомендацию
        bot.send_message(message.chat.id,
                         text=text_send,
                         parse_mode='Markdown',
                         reply_markup=markup)

    if random.random() < 0.5:
        bot.send_message(message.chat.id,
                         text="Оцените пожалуйста рекомендацию",
                         parse_mode='Markdown',
                         reply_markup=markup)
