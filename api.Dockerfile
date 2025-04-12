FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir api
COPY api ./api
COPY migrations ./migrations
COPY resources ./resources

RUN rm ./api/config.dev.py

CMD ["flask", "run"]
