FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y vim wget git unzip

COPY ./ ./

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["bot.py"]
