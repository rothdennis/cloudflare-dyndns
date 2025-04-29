FROM python:3.13-alpine3.21

LABEL org.opencontainers.image.source="https://github.com/rothdennis/docker-cloudflare-dyndns"
LABEL org.opencontainers.image.description="Update Cloudflare DNS records with dynamic IP address"
LABEL org.opencontainers.image.authors="Dennis Roth"

ENV REFRESH_INTERVAL=300
ENV IPV6=False
ENV PROXIED=False

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py .

CMD ["python", "-u", "main.py"]