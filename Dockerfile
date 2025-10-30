FROM python:3.12-slim

WORKDIR /app
COPY tests .

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "mikufetch"]
