FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

RUN apt update && apt install --no-install-recommends -y build-essential libpq-dev

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_SYSTEM_PYTHON=true

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.11-slim-bookworm

RUN apt update && \
    apt install --no-install-recommends -y libpq-dev locales && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen

COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/src

RUN python api/manage.py collectstatic --noinput
CMD python api/manage.py migrate && gunicorn -c api/delivery/gunicorn.conf.py api.delivery.wsgi:application