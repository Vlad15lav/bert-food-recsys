FROM python:3.10
WORKDIR /home/app

RUN apt-get update && apt-get install -y vim wget git unzip

COPY ./ ./

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["streamlit"]
CMD ["run", "Home_Chat.py"]