FROM python:3.9.6-slim
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000