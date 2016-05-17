FROM python:2.7

RUN pip install hero

ENTRYPOINT ["hero"]
