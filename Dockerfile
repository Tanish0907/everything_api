FROM python:3.11.4-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD [ "sh","-c","uvicorn Api:app --port=8000 --host=0.0.0.0" ]
