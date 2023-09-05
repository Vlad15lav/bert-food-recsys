# Рекомендательная система рецептов блюд
Этот кейс представляет собой рекомендательную систему рецептов блюд. В проекте использованы технологии веб-скрэпинга для сбора данных и fine-tuning модели трансформер BERT для получения эмбеддингов блюд. Кроме того, применяется метод TF-IDF в качестве второго способа подхода Content-based Filtering.

## Оглавление
[1. Постановка задачи](https://github.com/Vlad15lav/food-recsys#постановка-задачи)  
[2. Извлечения данных](https://github.com/Vlad15lav/food-recsys#извлечение-данных)  
[3. Построение рекомендательной системы](https://github.com/Vlad15lav/food-recsys/blob/main/README.md#построение-рекомендательной-системы)  
[4. Офлайн оценка рекомендательных систем](https://github.com/Vlad15lav/food-recsys/blob/main/README.md#офлайн-оценка-рекомендательных-систем)  
[5. Развертывание модели](https://github.com/Vlad15lav/food-recsys/blob/main/README.md#развертывание-модели)  
&nbsp; [5.1. Telegram бот](https://github.com/Vlad15lav/food-recsys/blob/main/README.md#telegram-бот)    
&nbsp; [5.2. Web приложение Streamlit](https://github.com/Vlad15lav/food-recsys/blob/main/README.md#web-приложение-streamlit)    
&nbsp; [5.3. Docker](https://github.com/Vlad15lav/food-recsys/blob/main/README.md#docker)   
[6. Онлайн A/B тестирование](https://github.com/Vlad15lav/food-recsys#онлайн-ab-тестирование)  

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
df.head()
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

Посмотреть визуализацию обучения модели можно с помощью логов tensorboard. 
```properties
load_ext tensorboard
%tensorboard --logdir tb_logs/bert-food
```

**TF-IDF** (Term Frequency-Inverse Document Frequency) - это [метод](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) для оценки важности слов в документе на основе их частоты в документе и коллекции документов. Я [использовал TF-IDF](demo_tfidf_recsys.ipynb) для создания векторного представления блюд на основе их текстового описания. Это позволяет учитывать важность слов и их контекст в тексте рецептов при вычислении сходства между ними.

Для измерения сходства между блюдами на основе их эмбеддингов, применяется косинусное сходство [(cosine similarity)](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html).


## Офлайн оценка рекомендательных систем

Для [оценка](eval_recsys.ipynb) эффективности рекомендательных систем на основе методов BERT и TF-IDF была использована метрика MAP@K (Mean Average Precision at K), которая учитывает точность рекомендаций на разных позициях в ранжированном списке. Для упрощения, релевантными рецептами считались те, которые принадлежали к одному классу.

| Метрика | BERT RecSys | TF-IDF RecSys |
|---------|-------------|---------------|
| MAP@3   | 0.849       | 0.753         |
| MAP@5   | 0.844       | 0.748         |
| MAP@7   | 0.839       | 0.736         |
| MAP@10  | 0.833       | 0.720         |

Комментарий: Модель BERT демонстрирует отличные результаты в рекомендации блюд одного класса, а TF-IDF, чаще, предоставлять более релевантные рекомендации по составу и способу приготовления. В зависимости от конкретной задачи и требований, можно выбрать подходящую модель для рекомендательной системы. Для объективной оценки и сравнения результатов рекомендательных систем, в дальнейшем будет проведено A/B тестирование. Это позволит сравнить оба метода на реальных пользователях и получить статистически значимые результаты, которые помогут сделать более обоснованный выбор между двумя подходами.

## Развертывание модели

### Requirements
Установите или обновите все необходимые пакеты, указанные в файле requirements.txt, чтобы убедиться, что проект имеет все необходимые зависимости для правильной работы.
```bash
pip install -U -r requirements.txt
```

### Telegram бот

<img src="./imgs/telebot-example.png" alt="Пример взаимодействия с Telegram ботом" width="512"/>

В файле `config.py` необходимо указать свои параметры базы данных и токен, полученный от [BotFather](https://t.me/BotFather).
```python
CONFIG = {
    "TOKEN": "YOUR TOKEN",
    "DATABASE": {
        "host": "YOUR HOST",
        "user": "YOUR USER",
        "passwd": "YOUR PASSWD",
        "database": "YOUR DATABASE NAME"
    },
    ...
``` 

Скачайте необходимые файлы для запуска моделей и векторные представления рекомендации контекста блюд.
```bash
gdown https://drive.google.com/uc?id=17nDmHE84dT76vsVrq-5RaqrEoJBdFMV7

unzip -x recsys_data.zip

wget -O weights/bert-food-cls.pth https://github.com/Vlad15lav/food-recsys/releases/download/v0.1.0/bert-food-cls.pth
```

Запустите Telegram бота с помощью скрипта `bot.py`.
```bash
python bot.py
``` 

### Web приложение Streamlit

<img src="./imgs/web-app-example.png" alt="Пример взаимодействия с Web приложением" width="768"/>

Сервис доступен на сайте [streamlit.app](https://food-recsys-chat.streamlit.app/).

Запустите Web приложение с помощью команды, указав название скрипта `Home_Chat.py`.
```bash
streamlit run Home_Chat.py
```

### Docker
Чтобы запустить приложение на Docker, вам потребуется выполнить следующие шаги:

Создаем сеть для контейнеров:  
```bash
docker network create -d bridge my-net
```

Создаем volume для хранения данных СУБД:
```bash
docker volume create db_volume
```

Запускаем контейнер базу данных MySQL:  
```bash
docker run --name database \
    --network my-net \
    -v db_volume:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=<my-secret-pw> \
    -e MYSQL_USER=<my-user> \
    -e MYSQL_PASSWORD=<my-password> \
    -e MYSQL_DATABASE=aichef \
    -d \
    mysql:8.0.32 
```

Создаем образ и контейнер для Телеграм бота:
```bash
docker build -t mybot:1.0.0 .
```

```bash
docker run --name my_bot \
    --network my-net \
    -e TELEGRAM_TOKEN=<my-tg-token> \
    -e DATABASE_HOST=database \
    -e DATABASE_USER=<my-user> \
    -e DATABASE_PASSWORD=<my-password> \
    -e DATABASE_NAME=aichef \
    -d \
    mybot:1.0.0
```

### Docker Compose
Запустить базу данных MySQL и основной контейнер Телеграм бота можно сразу с помощью docker-compose файла.  

Перед запуском укажите `<переменные окружения>`:
```yaml
services:
  database:
    environment:
      MYSQL_ROOT_PASSWORD: <YOUR_ROOT_PASSWORD> # Пароль для ROOT
      MYSQL_USER: <YOUR_USER> # Имя пользователя БД
      MYSQL_PASSWORD: <YOUR_PASSWORD> # Пароль пользователя БД
      MYSQL_DATABASE: aichef

  telebot:
    environment:
      TELEGRAM_TOKEN: <YOUR_TG_TOKEN> # Ваш токен BotFather
      DATABASE_HOST: database
      DATABASE_USER: <YOUR_USER> # Имя пользователя БД
      DATABASE_PASSWORD: <YOUR_PASSWORD> # Пароль пользователя БД
      DATABASE_NAME: aichef
```
Соберите образ для приложения и запустите проект.
```bash
docker build -t mybot:1.0.0 .
```
```bash
docker-compose run -d
```

## Онлайн A/B тестирование
В данный момент проводится A/B тестирование рекомендательной системы BERT по сравнению со старой TF-IDF, ожидается нужный размер выборки.

ВНИМАНИЕ: описание этого README периодический обновляется
