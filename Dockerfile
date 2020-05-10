FROM python:3.7.3-slim

COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["sh","./gunicorn_starter.sh"]
