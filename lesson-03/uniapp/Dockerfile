FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY lesson-03/uniapp /app

ENV PYTHONUNBUFFERED=1

EXPOSE 8001

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "--workers", "2", "uniapp.wsgi:application"]
