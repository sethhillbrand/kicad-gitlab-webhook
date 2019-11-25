FROM alpine:3.8

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
COPY server.py /app

RUN apk add --update --no-cache python3
RUN pip3 install -r requirements.txt
RUN rm requirements.txt

USER 1000

CMD [ "gunicorn", "--workers=4", "-b 0.0.0.0:5000", "server:app" ]
EXPOSE 5000
