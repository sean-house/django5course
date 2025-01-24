FROM python:3.13-bullseye AS base
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install -y gettext

RUN mkdir /code

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml ./

COPY . .

FROM base AS development

RUN poetry install
RUN poetry run playwright install --with-deps

RUN chmod +x start-django.sh

EXPOSE 8000

ENTRYPOINT [ "/code/start-django.sh" ]

FROM base AS production

RUN poetry install --only main

RUN chmod +x start-django.sh

EXPOSE 8000

ENTRYPOINT [ "/code/start-django.sh" ]
