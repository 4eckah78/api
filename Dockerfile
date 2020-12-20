FROM python:3.8

ENV PYTHONUNBUFFERED 1


# RUN pip install
RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
