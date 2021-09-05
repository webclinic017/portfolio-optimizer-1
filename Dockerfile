FROM python:3.9 as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/venv/bin:${PATH}" \
    VIRTUAL_ENV=/venv

WORKDIR /app
RUN useradd -m app && chown -R app:app /app && pip install -U pip poetry && python -m venv /venv

COPY poetry.lock pyproject.toml ./
RUN poetry install -v --no-dev

COPY --chown=app . ./
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM python:3.9-slim-bullseye as final

ENV PATH="/venv/bin:${PATH}" VIRTUAL_ENV=/venv

RUN useradd -m app
COPY --from=builder --chown=app /venv /venv
USER app

EXPOSE 5000
CMD ["/venv/bin/python", "-m", "gunicorn", "-c", "python:portfolio_optimization.guniconf", "portfolio_optimization.app:create_app"]
