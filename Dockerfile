FROM python:latest
RUN apt update
WORKDIR /opt/app
COPY ./requirements.txt /opt/app
RUN ls && pip3 install -r requirements.txt
COPY . /opt/app
CMD python3 bot.py
