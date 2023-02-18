FROM python:3.8-slim

COPY test/cassandra-setup/requirements.txt .
RUN pip install -r requirements.txt

COPY test/cassandra-setup/setup.py .
