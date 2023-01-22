FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /webtronics_task

COPY requirements.txt /webtronics_task
COPY boot.sh .

RUN pip3 install --upgrade pip setuptools==57.5.0
RUN pip3 install --upgrade pip -r requirements.txt
RUN chmod +x boot.sh

COPY ./ .

RUN chmod +x /webtronics_task/boot.sh
