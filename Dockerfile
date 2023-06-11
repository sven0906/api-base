FROM python:3.7-alpine
MAINTAINER Deven Ltd

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

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web

RUN chown -R user:user /app/
RUN chmod -R 755 /app/logs
USER user



# DB연결되기까지 20초 대기시간 걸어놓기
ENTRYPOINT ["dockerize", "-wait", "tcp://mysql_service:3306", "-timeout", "23s"]
