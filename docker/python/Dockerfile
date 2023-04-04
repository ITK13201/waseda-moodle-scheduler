FROM python:3.11-buster AS development

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

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

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

RUN mkdir /gunicorn
COPY ./config/gunicorn /gunicorn

CMD ["gunicorn", "-c", "/gunicorn/gunicorn.py"]
