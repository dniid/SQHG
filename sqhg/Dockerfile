FROM python:3.11

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR "/usr/src/app"
STOPSIGNAL SIGINT

ARG MODE

EXPOSE 8000

COPY ["requirements/", "docker/build.sh", "/tmp/"]
RUN sh /tmp/build.sh /tmp/

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

ADD [".", "/usr/src/app"]
