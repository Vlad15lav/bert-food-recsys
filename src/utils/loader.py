import os
import gdown
import pickle
import torch
import numpy as np
import pandas as pd
import scipy.sparse as sparse
import wget
import zipfile

from torch import nn
from transformers import BertConfig, \
                        BertForSequenceClassification, BertTokenizer
from config import CONFIG


def load_files():
    if not (os.path.exists(CONFIG["DATA_ITEMS"]) and
            os.path.exists(CONFIG["TFIDF_ITEMS_PATH"]) and
            os.path.exists(CONFIG["TFIDF_FEATURES"])):

        gdown.download("https://drive.google.com/" +
                       "uc?id=17nDmHE84dT76vsVrq-5RaqrEoJBdFMV7",
                       "recsys_data.zip", quiet=False)

        with zipfile.ZipFile("recsys_data.zip", 'r') as zip_ref:
            zip_ref.extractall(".")

        os.remove("recsys_data.zip")
        wget.download("https://github.com/Vlad15lav/food-recsys" +
                      "/releases/download/v0.1.0/bert-food-cls.pth",
                      out="weights/bert-food-cls.pth")


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
    tfidf_model = pickle.load(open(CONFIG["TFIDF_FEATURES"], "rb"))

    return tfidf_model


def load_model_bert():
    """
    Загрузка модели BERT и Tokenizer
    """
    model = BertForSequenceClassification(BertConfig(**CONFIG["BERT_CONFIG"]))
    model.classifier = nn.Linear(312, 13)

    model.load_state_dict(torch.load(CONFIG["BERT_WEIGHT"],
                                     map_location='cpu'))
    model = model.bert.eval()

    tokenizer = BertTokenizer.from_pretrained(CONFIG["TOKENIZER_PATH"])

    return model, tokenizer
