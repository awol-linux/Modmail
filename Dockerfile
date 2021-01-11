FROM python:latest 

COPY . /opt/app
WORKDIR /opt/app
RUN apt update && apt install python3-pip gcc python3-dev -y  && pip3 install -r requirements.txt
CMD python3 bot.py
