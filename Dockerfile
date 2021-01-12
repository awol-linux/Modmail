FROM python:latest 

# RUN apt update && apt install python3-pip gcc python3-dev -y
WORKDIR /opt/app
COPY ./requirements.txt /opt/app
RUN ls && pip3 install -r requirements.txt
COPY . /opt/app
CMD python3 bot.py
