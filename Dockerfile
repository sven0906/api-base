FROM python:3.7-alpine
MAINTAINER Deven Ltd

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFRERED 1

COPY ./requirements.txt /requirements.txt
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
RUN pip install -r /requirements.txt

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN mkdir -p /app

RUN addgroup -S app && adduser -S app -G app

ENV APP_HOME=/app
WORKDIR $APP_HOME
COPY ./app $APP_HOME
RUN python manage.py collectstatic --no-input

RUN chown -R app:app $APP_HOME

USER app

# DB연결되기까지 20초 대기시간 걸어놓기
ENTRYPOINT ["dockerize", "-wait", "tcp://mysql_service:3306", "-timeout", "23s"]
