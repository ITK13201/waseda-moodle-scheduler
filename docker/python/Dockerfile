ARG ubuntu_version=22.04
ARG python_version=3.11

FROM ubuntu:${ubuntu_version} as tools

ARG dockerize_version=v0.6.1

RUN apt update \
    && apt install -y wget
RUN wget https://github.com/jwilder/dockerize/releases/download/${dockerize_version}/dockerize-linux-amd64-${dockerize_version}.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-${dockerize_version}.tar.gz \
    && rm dockerize-linux-amd64-${dockerize_version}.tar.gz

FROM python:${python_version}-buster AS development

ARG APP_NAME=waseda-moodle-scheduler

ENV PYTHONDONTWRITEBITECOTE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /${APP_NAME} \
    && mkdir -p /var/log/${APP_NAME}

WORKDIR /${APP_NAME}

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install pipenv

COPY ./${APP_NAME}/Pipfile ./Pipfile
COPY ./${APP_NAME}/Pipfile.lock  ./Pipfile.lock

RUN pipenv install --ignore-pipfile --deploy --system --dev

COPY ./${APP_NAME} .
COPY ./docker/python/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY --from=tools /usr/local/bin/dockerize /usr/local/bin

ENTRYPOINT ["sh", "/usr/local/bin/entrypoint.sh"]
CMD ["-d", "-w", "-m"]

FROM python:3.11-buster AS production

ARG APP_NAME=waseda-moodle-scheduler

ENV PYTHONDONTWRITEBITECOTE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /${APP_NAME} \
    && mkdir -p /var/log/${APP_NAME}

WORKDIR /${APP_NAME}

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install pipenv

COPY ./${APP_NAME}/Pipfile ./Pipfile
COPY ./${APP_NAME}/Pipfile.lock ./Pipfile.lock

RUN pipenv install --ignore-pipfile --deploy --system

COPY ./${APP_NAME} .
COPY ./docker/python/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY --from=tools /usr/local/bin/dockerize /usr/local/bin

RUN mkdir /gunicorn
COPY ./config/gunicorn /gunicorn

ENTRYPOINT ["sh", "/usr/local/bin/entrypoint.sh"]
CMD ["-w", "-m"]
