FROM python:3.13-bullseye
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install -y gettext

RUN mkdir /code

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .

EXPOSE 8000

ENTRYPOINT [ "poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000" ]
