FROM python:3.8

RUN apt-get update

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY entry /app/entry
RUN chmod a+x /app/entry

COPY manage.py /app/manage.py
COPY marketing /app/marketing

WORKDIR /app
ENTRYPOINT ["/app/entry"]
