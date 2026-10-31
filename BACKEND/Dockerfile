FROM python:3.13-slim AS builder

RUN mkdir /app

WORKDIR /app

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip 

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

#produccion
FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

#USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

# Run the application.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "agenda.wsgi:application"]