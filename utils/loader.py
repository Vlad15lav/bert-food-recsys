import pickle
import torch
import nltk
import numpy as np
import pandas as pd
import scipy.sparse as sparse

from torch import nn
from transformers import BertConfig, BertForSequenceClassification, BertTokenizer
from config import CONFIG

from sklearn.feature_extraction.text import TfidfVectorizer

from pymystem3 import Mystem
from nltk.corpus import stopwords


def load_data():
    """
    Чтение данных набора данных и эмбеддингов
    """
    data_items = pd.read_csv(CONFIG["DATA_ITEMS"])

    bert_embed_items = np.load(CONFIG["BERT_ITEMS_PATH"])
    tfidf_embed_items = sparse.load_npz(CONFIG["TFIDF_ITEMS_PATH"])

    return data_items, bert_embed_items, tfidf_embed_items

def load_model_tfidf():
    """
    Загрузка модели TF-IDF
    """
    # ifile = open("data/tf-idf-model1.pkl", "rb")
    # tfidf_model = dill.load(ifile)
    # ifile.close()
    tfidf_model = pickle.load(open(CONFIG["TFIDF_FEATURES"], "rb"))
    
    return tfidf_model

# def load_model_tfidf():
#     """
#     Загрузка модели TF-IDF
#     """
#     datdf_itemsa_items = pd.read_csv(CONFIG["DATA_ITEMS"])
#     stopwords_ru = stopwords.words("russian")
#     mystem = Mystem()
    
#     text_list = []
#     for i in range(df_items.shape[0]):
#         text = " ".join(df_items.iloc[i, :5].values)

#         # Фильтруем текст
#         text = text.lower()
#         text = re.sub(r'\([^()]*\)', '', text)
#         text = re.sub(r'[^а-яё]', ' ', text)
#         text = re.sub(" +", " ", text)

#         tokens = mystem.lemmatize(text) # Нормализуем слова
#         # Убираем стоп-слова
#         text = " ".join([token for token in tokens\
#                          if not token in stopwords_ru and token != " " and len(token) > 1])

#         text_list.append(text)

#     print("Wights loaded!")

#     index_set = np.arange(len(text_list))

#     np.random.seed(42)
#     np.random.shuffle(index_set)

#     train_index = index_set[:-int(len(index_set) * 0.2)]
#     train_set = [text_list[i] for i in train_index]

#     tfidf_model = TfidfVectorizer()
#     tfidf_model.fit(train_set)

#     return tfidf_model

def load_model_bert():
    """
    Загрузка модели BERT и Tokenizer
    """    
    model = BertForSequenceClassification(BertConfig(**CONFIG["BERT_CONFIG"]))
    model.classifier = nn.Linear(312, 13)

    model.load_state_dict(torch.load(CONFIG["BERT_WEIGHT"], map_location='cpu'))
    model = model.bert.eval()

    tokenizer = BertTokenizer.from_pretrained(CONFIG["TOKENIZER_PATH"])

    return model, tokenizer