FROM python:3

RUN mkdir -p /home/app

WORKDIR /home/app

COPY requirements.txt /home/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
