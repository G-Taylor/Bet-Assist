FROM python:3.11-rc-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --upgrade wheel
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python3", "app/app.py"]