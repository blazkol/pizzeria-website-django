# Stage 1: Base build stage
FROM python:3.11-slim AS builder
RUN mkdir /app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim
RUN useradd -m -r appuser && \
   mkdir /app && \
   mkdir /app/staticfiles && \
   chown -R appuser /app
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8000
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
