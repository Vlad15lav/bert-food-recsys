import os
import re
import nltk
import gdown
import pickle
import pandas as pd
import numpy as np
import streamlit as st
import scipy.sparse as sparse
import zipfile

from config import CONFIG

from streamlit_chat import message

from nltk.corpus import stopwords
from pymystem3 import Mystem
from sklearn.metrics.pairwise import cosine_similarity

BOT_MESSAGE_TEMP = (
    "Настоятельно рекомендую ознакомиться с такими рецептами:\n\n",
    "Не упустите возможность попробовать следующие рецепты:\n\n",
    "Хотел бы поделиться с вами несколькими интересными рецептами, " +
    "например...\n\n",
    "Позвольте порекомендовать вам некоторые восхитительные рецепты, " +
    "включая...\n\n",
    "С радостью предложу вам набор рецептов, в том числе...\n\n",
    "Рекомендую присмотреться к таким интересным рецептам:\n\n",
    "Предлагаю рассмотреть следующие рецепты, которые обязательно " +
    "стоит попробовать:\n\n",
    "Могу порекомендовать несколько вкусных рецептов, среди которых...\n\n",
    "Вот несколько замечательных рецептов, которые рекомендую " +
    "попробовать:\n\n",
    "Попробуйте обратить внимание на следующие интересные рецепты:\n\n"
    )

st.set_page_config(
        page_title="AI Chef | Chat",
        page_icon="📝",
        layout="wide"
    )

if not (os.path.exists(CONFIG["DATA_ITEMS"]) and
        os.path.exists(CONFIG["TFIDF_ITEMS_PATH"]) and
        os.path.exists(CONFIG["TFIDF_FEATURES"])):

    gdown.download("https://drive.google.com/" +
                   "uc?id=17nDmHE84dT76vsVrq-5RaqrEoJBdFMV7",
                   "recsys_data.zip", quiet=False)

    with zipfile.ZipFile("recsys_data.zip", 'r') as zip_ref:
        zip_ref.extractall(".")


@st.cache_data
def load_model():
    data_items = pd.read_csv(CONFIG["DATA_ITEMS"])
    tfidf_embed_items = sparse.load_npz(CONFIG["TFIDF_ITEMS_PATH"])
    tfidf_model = pickle.load(open(CONFIG["TFIDF_FEATURES"], "rb"))

    nltk.download("stopwords")
    stopwords_ru = stopwords.words("russian")
    mystem = Mystem()
    return data_items, tfidf_embed_items, tfidf_model, stopwords_ru, mystem


def get_tfidf_recomendation(text, model, embed_items):
    """
    Вычисления схожих продуктов для рекомендации с помощью TF-IDF
    """
    # Фильтрация текста
    text = text.lower()
    text = re.sub(r'\([^()]*\)', '', text)
    text = re.sub(r'[^а-яё]', ' ', text)
    text = re.sub(" +", " ", text)

    # Удаляем стоп-слова и нормализуем
    tokens = mystem.lemmatize(text)
    text = " ".join([token for token in tokens
                     if token not in stopwords_ru and
                     token != " " and len(token) > 1])

    # Векторное представление TF-IDF модели
    out = model.transform([text])

    # Получаем схожесть рецептов и сортируем по значению
    rating = cosine_similarity(embed_items, out).reshape(-1)
    rating_arg = np.argsort(rating)[::-1]

    return rating_arg


data_items, tfidf_embed_items, tfidf_model, stopwords_ru, mystem = load_model()


def main():
    st.title("AI Chef Chat")
    with st.expander("Подробнее о приложении"):
        st.write("AI Chef - это чат-бот, разработанный для предоставления " +
                 "персонализированных рекомендаций по приготовлению " +
                 "разнообразных блюд. Благодаря использованию модели " +
                 "машинного обучения и анализу предпочтений пользователей " +
                 ", ассистент предлагает уникальные рецепты, " +
                 "соответствующие вкусам и предпочтениям " +
                 "каждого пользователя.")

    # Создаем переменную сессии, если чат был только создан
    if "messages" not in st.session_state:
        st.session_state.messages = []
        start_message = "Привет! Я – AI Chef. С моей помощью вы можете "\
            "удобнее и быстрее подобрать для себя рецепт блюда. "\
            "Присылайте ваши пожелания, "\
            "а я порекомендую подходящий рецепт. Примеры запросов: "\
            "«Предложи что-нибудь из помидоров, "\
            "лука и курицы» или «Десерт из шоколада и фруктов»."

        st.session_state.messages.append({"role": "assistant",
                                          "content": start_message})

    # Отоброжаем историю чата из переменной сессии
    for i in range(len(st.session_state.messages)):
        msg = st.session_state.messages[i]
        if msg['role'] == 'assistant':
            message(msg['content'], key=str(i))
        else:
            message(msg['content'], is_user=True, key=str(i) + '_user')

    # Считываем текстовый запрос пользователя
    if prompt := st.chat_input("Напиши что нибудь"):
        key_index = len(st.session_state.messages) + 1
        st.session_state.messages.append({"role": "user", "content": prompt})
        message(prompt, is_user=True, key=str(key_index) + '_user')

        # Создаем ответ Chat бота
        rating_arg = get_tfidf_recomendation(prompt,
                                             tfidf_model,
                                             tfidf_embed_items)
        response = np.random.choice(BOT_MESSAGE_TEMP)
        for i in range(3):
            item_id = int(rating_arg[i])

            response += "Название: {}\nСостав: {}\n{}. Время готовки: {}" \
                .format(*data_items.loc[[item_id], [
                    'name',
                    'ingredient',
                    'type_kitchen',
                    'time_cook']
                ].values.reshape(-1))
            response += "\n\nПодробнее рецепт по [ссылке]" \
                f"({data_items.loc[item_id, 'link']})\n\n"

        response = response.rstrip("\n\n")

        st.session_state.messages.append({"role": "assistant",
                                          "content": response})
        message(response, key=str(key_index))


if __name__ == "__main__":
    main()
