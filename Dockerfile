FROM python:3.9.0rc2-alpine3.12

WORKDIR /opt/app

ARG environment

COPY . .

RUN apk add --update alpine-sdk && \
    pip install -r requirements.txt

CMD [ "python", "bot.py" ]