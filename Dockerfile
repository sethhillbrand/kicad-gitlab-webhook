FROM alpine:3.8

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN apk add --update --no-cache python3
RUN pip3 install -r requirements.txt

CMD [ "gunicorn", "--workers=4", "-b 0.0.0.0:5000", "server:app" ]
EXPOSE 5000