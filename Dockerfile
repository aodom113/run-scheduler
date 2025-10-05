FROM python:3-alpine AS base

RUN apk add --no-cache make

ENV VENV=/user/bin/venv
RUN python -m venv ${VENV}
ENV PATH=${VENV}/bin:${PATH}
RUN python -m pip install --upgrade pip \
    && python -m pip install poetry

WORKDIR /workspace/run-scheduler
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    poetry install --no-root

FROM base AS dev

RUN apk add git
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    poetry install --no-root --all-extras

FROM base

COPY . .
RUN poetry install
EXPOSE 80
