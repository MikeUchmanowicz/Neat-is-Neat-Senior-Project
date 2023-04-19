FROM python:3.9-alpine

WORKDIR /WebApp

COPY requirements.txt .

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev && \
    apk add mariadb-dev && \
    pip install -r requirements.txt && \
    apk del build-deps

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
