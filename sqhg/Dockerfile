FROM python:3.11

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR "/usr/src/app"
STOPSIGNAL SIGINT

ARG MODE

EXPOSE 8000

COPY [".", "/usr/src/app"]
RUN sh docker/build.sh requirements
