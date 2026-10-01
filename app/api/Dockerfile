# Контекст сборки — корень репозитория (см. infra/compose.yaml).

# 1. Сборка переиспользуемого пакета order-core в wheel — без приложения.
FROM python:3.10-slim AS core-build
WORKDIR /build
RUN pip install --no-cache-dir build
COPY packages/core ./core
RUN python -m build ./core --wheel --outdir /dist

# 2. Образ приложения: зафиксированные зависимости + wheel ядра + код API.
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY app/api/requirements.lock ./requirements.lock
RUN pip install --no-cache-dir -r requirements.lock

COPY --from=core-build /dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

COPY app/api ./api
RUN pip install --no-cache-dir --no-deps ./api

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "order_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
