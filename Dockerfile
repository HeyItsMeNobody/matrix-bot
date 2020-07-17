FROM python:3.8-buster

MAINTAINER Dyon "dyon@dyonb.nl"

# Install npm
RUN apt-get update
RUN apt-get install libolm2 libolm-dev

COPY ./ /

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]