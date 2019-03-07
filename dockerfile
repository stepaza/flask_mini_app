FROM python:3.6-alpine

RUN adduser -D shopper

WORKDIR /home/shopper

COPY requirements.txt /home/shopper/requirements.txt

RUN python -m venv todo_venv

RUN todo_venv/bin/pip install --proxy="INSEL\I0308559:InselSPZ990@proxy.insel.ch" -r requirements.txt
RUN todo_venv/bin/pip install --proxy="INSEL\I0308559:InselSPZ990@proxy.insel.ch" gunicorn

COPY main.py main.py
COPY wsgi.py wsgi.py
COPY api_test.py api_test.py
COPY boot.sh ./
RUN chmod +x /home/shopper/boot.sh

RUN chown -R shopper:shopper ./
USER shopper


ENTRYPOINT ["/home/shopper/boot.sh"]

