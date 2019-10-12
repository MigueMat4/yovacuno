FROM python:3
MAINTAINER Miguel
ENV PYTHONUNBUFFERED 1
#ENV C_FORCE_ROOT true
RUN mkdir /src
RUN mkdir /static
WORKDIR /src
ADD . /src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn psx.wsgi -b 0.0.0.0:8000
