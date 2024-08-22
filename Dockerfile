FROM python:3.12-slim AS builder
RUN apt-get update && apt-get -y upgrade

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PDM_CHECK_UPDATE=false \
    PYTHONUNBUFFERED=1
RUN useradd --create-home app
USER app
WORKDIR /home/app/

RUN pip install --user pdm

COPY pyproject.toml pdm.lock README.md ./
RUN ~/.local/bin/pdm install --check --prod --no-editable

FROM python:3.12-slim
RUN apt-get update && apt-get -y upgrade

ENV PATH="/home/app/.venv/bin:$PATH"
RUN useradd --create-home app
USER app
WORKDIR /home/app/

COPY --from=builder /home/app/.venv/ ./.venv/
COPY --chown=app:app enxame/ /home/app/enxame/

CMD fastapi run enxame
