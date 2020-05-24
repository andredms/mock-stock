FROM python:3.7.7

WORKDIR /bot

COPY './requirements.txt' .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "bot.py"]
