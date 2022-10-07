FROM python:3.8-alpine

# set environment varibles
ENV TZ=Africa/Johannesburg
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=true

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /usr/local/zms/zms-api

COPY ./requirements.txt ./

# Install required packages
RUN apk upgrade \
    && apk update \
    && apk add build-base \
    && apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc curl \
    && apk add mariadb-dev \
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk del build-deps

RUN pip install pip==22.0.4 && pip install --upgrade setuptools wheel && pip install -r requirements.txt

COPY  . /usr/local/zms/zms-api

# Make port 8000 available to the world outside this container
EXPOSE 8000

RUN pip install -e .

ENTRYPOINT uwsgi --ini-paste "/usr/local/zms/zms-api/zimsend/config/pyramid/dev.ini"
