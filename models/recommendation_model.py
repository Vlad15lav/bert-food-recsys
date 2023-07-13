import re
import torch
import numpy as np
import nltk

from nltk.corpus import stopwords
from pymystem3 import Mystem
from sklearn.metrics.pairwise import cosine_similarity

from config import CONFIG

nltk.download("stopwords")
stopwords_ru = stopwords.words("russian")
mystem = Mystem()

def get_bert_recommendation(text, tokenizer, model, embed_items):
    """
    Вычисления схожих продуктов для рекомендации с помощью BERT
    """
    text_tokens = tokenizer(text, **CONFIG['TOKENIZER'])

    with torch.no_grad():
        out = model(**text_tokens)
        out = out.last_hidden_state[:, 0, :].cpu().numpy()

    rating = cosine_similarity(embed_items, out).reshape(-1)
    rating_arg = np.argsort(rating)[::-1]
    
    return rating_arg


def get_tfidf_recomendation(text, model, embed_items):
    """
    Вычисления схожих продуктов для рекомендации с помощью TF-IDF
    """
    text = text.lower()
    text = re.sub(r'\([^()]*\)', '', text)
    text = re.sub(r'[^а-яё]', ' ', text)
    text = re.sub(" +", " ", text)

    tokens = mystem.lemmatize(text)
    text = " ".join([token for token in tokens\
                    if not token in stopwords_ru and token != " " and len(token) > 1])
    out = model.transform([text])

    rating = cosine_similarity(embed_items, out).reshape(-1)
    rating_arg = np.argsort(rating)[::-1]
    
    return rating_arg