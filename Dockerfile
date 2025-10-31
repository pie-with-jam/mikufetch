FROM python:3.12-slim

# Optional: tools for better GPU/Resolution detection inside the container
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       x11-xserver-utils \
       mesa-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY tests .

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "mikufetch"]
