FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "app/app.py" ]