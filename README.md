# Рекомендательная система рецептов блюд
Этот кейс представляет собой рекомендательную систему рецептов блюд. В проекте использованы технологии веб-скрэпинга для сбора данных и fine-tuning модели трансформер BERT для получения эмбеддингов блюд. Кроме того, применяется метод TF-IDF в качестве второго способа подхода Content-based Filtering.

## Постановка задачи
Цель проекта - разработать рекомендательную систему, которая предлагает пользователям рекомендацию рецептов блюд на основе их предпочтений.

1. **Ввод текста от пользователя**: Пользователь вводит текстовую информацию, связанную с рецептами или блюдами. Это может быть название блюда, список ингредиентов, описание или любой другой текст, связанный с кулинарией.

2. **Поиск похожих рецептов**: На основе введенного текста система проводит поиск и анализирует набор данных рецептов или блюд. Используя различные методы и алгоритмы, система определяет наиболее похожие рецепты или блюда, основываясь на семантическом сходстве текстовой информации.

3. **Предложение рекомендаций**: Система предлагает пользователю список рекомендаций, включающий рецепты или блюда, которые наиболее соответствуют введенному тексту. Рекомендации могут быть ранжированы по степени сходства или другими факторами, учитывая предпочтения пользователя, доступные ингредиенты и другие факторы, в зависимости от реализации системы.

## Извлечение данных
Для получения описания рецептов различных блюд с [сайта](https://www.eda.ru), использовалась технология [веб-скрэпинга](data-parser.ipynb). Это позволило автоматически извлечь информацию с веб-страниц, в данном случае, описания рецептов блюд. Итоговый созданный набор данных был загружен и доступен по [ссылке](https://www.kaggle.com/datasets/vlad15lav/recipes-corpus-textual-data-for-nlprecsys) на платформе Kaggle. 
```python
import pandas as pd

df = pd.DataFrame('food-dataset-ru.csv')
print(df.head())
```
| name                        | text                                                  | ingredient                                          | energy                                              | type_kitchen       | time_cook      | link                                                 | label    |
|-----------------------------|-------------------------------------------------------|-----------------------------------------------------|-----------------------------------------------------|--------------------|----------------|------------------------------------------------------|----------|
| Завтрак для ленивых        | В широкую миску выложить творог, добавить яйцо...     | Куриное яйцо: 1 штука, Мягкий творог: 200 г, П...   | Калорий 87 ккал, Белки 8 грамм, Жиры 2 грамм, ...   | Русская кухня      | 15 минут       | [ссылка](https://eda.ru/recepty/zavtraki/zavtrak-dlja-lenivih-21975) | Завтрак  |
| Гречневый завтрак          | Гречку промыть, залить 2 стаканами кипятка, по...     | Гречневая крупа: 1 стакан, Рубленая петрушка: ...   | Калорий 284 ккал, Белки 6 грамм, Жиры 11 грамм...   | Русская кухня      | 1 час 20 минут | [ссылка](https://eda.ru/recepty/zavtraki/grechnevij-zavtrak-22397) | Завтрак  |
| Завтрак детства            | Морковь и зеленое яблоко натереть на средней т...     | Морковь: 1 штука, Яблоко: 1 штука, Апельсины: ...   | Калорий 623 ккал, Белки 13 грамм, Жиры 22 грам...   | Русская кухня      | 5 минут        | [ссылка](https://eda.ru/recepty/zavtraki/zavtrak-detstva-22998) | Завтрак  |
| Полный английский завтрак  | Разогреть духовку до 180 градусов, а сковороду...     | Куриное яйцо: 2 штуки, Свиные сосиски: 2 штуки...   | Калорий 907 ккал, Белки 26 грамм, Жиры 75 грам...   | Британская кухня   | 30 минут       | [ссылка](https://eda.ru/recepty/polnyy-angliyskiy-zavtrak-20740) | Завтрак  |
| Французские гренки к завтраку | Смешать яйцо с молоком. Посолить. Обмакнуть ку...     | Батон: 3 куска, Молоко: 2 столовые ложки, Кури...   | Калорий 519 ккал, Белки 16 грамм, Жиры 29 грам...   | Французская кухня  | 10 минут       | [ссылка](https://eda.ru/recepty/zavtraki/francuzskie-grenki-k-zavtraku-32744) | Завтрак  |

## Построение рекомендательной системы

Для получения эмбеддингов блюд были использованы два подхода: BERT и TF-IDF.

**BERT** (Bidirectional Encoder Representations from Transformers) - это [модель](https://huggingface.co/docs/transformers/model_doc/bert) глубокого обучения, способная генерировать контекстные эмбеддинги для текстовых данных. В данном кейсе использовалась предобученная scratch модель [`rubert-tini2`](https://huggingface.co/cointegrated/rubert-tiny2) в качестве базовой модели BERT. С помощью fine-tuning, [обучил модель](train_embeddings.ipynb) на наборе данных рецептов для получения эмбеддингов блюд. Демонстрация полученных эмбеддингов показаны в [ноутбуке](demo_bert_recsys.ipynb).

**TF-IDF** (Term Frequency-Inverse Document Frequency) - это [метод](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) для оценки важности слов в документе на основе их частоты в документе и коллекции документов. Я [использовал TF-IDF](demo_tfidf_recsys.ipynb) для создания векторного представления блюд на основе их текстового описания. Это позволяет учитывать важность слов и их контекст в тексте рецептов при вычислении сходства между ними.

Для измерения сходства между блюдами на основе их эмбеддингов, применяется косинусное сходство [(cosine similarity)](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html).


## Оценка рекомендательных систем

Для оценки эффективности рекомендательных систем на основе методов BERT и TF-IDF была использована метрика MAP@K (Mean Average Precision at K), которая учитывает точность рекомендаций на разных позициях в ранжированном списке. Для упрощения, релевантными рецептами считались те, которые принадлежали к одному классу.

| Метрика | BERT RecSys | TF-IDF RecSys |
|---------|-------------|---------------|
| MAP@3   | 0.849       | 0.753         |
| MAP@5   | 0.844       | 0.748         |
| MAP@7   | 0.839       | 0.736         |
| MAP@10  | 0.833       | 0.720         |



## Requirements
Установите или обновите все необходимые пакеты, указанные в файле requirements.txt, чтобы убедиться, что проект имеет все необходимые зависимости для правильной работы.
```
pip install -U -r requirements.txt
```

ВНИМАНИЕ: описание этого README периодический обновляется
