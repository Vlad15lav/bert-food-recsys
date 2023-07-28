import io
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from config import CONFIG

st.set_page_config(
        page_title="AI Chef | Dataset",
        page_icon="📝",
        layout="wide",
    )

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

@st.cache_data
def load_df(path):
    return pd.read_csv(path)

data_items = load_df(CONFIG["DATA_ITEMS"])
csv = convert_df(data_items)

st.title("Dataset")

st.markdown("""Для получения описания рецептов различных блюд с [сайта](https://www.eda.ru),
                использовалась технология [веб-скрэпинга](https://github.com/Vlad15lav/food-recsys/blob/main/data-parser.ipynb).
                Это позволило автоматически извлечь информацию с веб-страниц, в данном случае, описания рецептов блюд.
                Итоговый созданный набор данных был загружен и доступен по 
                [ссылке](https://www.kaggle.com/datasets/vlad15lav/recipes-corpus-textual-data-for-nlprecsys) на платформе Kaggle.""")

st.download_button(
    label="Скачать Dataset",
    data=csv,
    file_name='food-dataset-ru.csv',
    mime='text/csv',
)

st.code('''import pandas as pd

df = pd.DataFrame('food-dataset-ru.csv')
print(df)''', language='python')
st.dataframe(data_items)

st.write("Информация о датасете:")
st.code('''df.info()''', language='python')
buffer = io.StringIO()
data_items.info(buf=buffer)
st.text(buffer.getvalue())

fig = plt.figure(figsize=(10, 4))
fig.suptitle("Размер классов")
ax = sns.countplot(x=data_items["label"])
plt.sca(ax)
plt.xlabel('Label')
plt.xticks(rotation=90)
plt.ylabel('Количество')
st.pyplot(fig)
