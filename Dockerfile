FROM python:3.9-slim-buster as base

RUN apt-get update &&  apt-get install -y \
 ca-certificates \
 git \
 tini \
 make \
 && rm -rf /var/lib/apt/lists/* 
 
ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT
ENV PATH=/pyroot/bin:$PATH

FROM base as builder

WORKDIR /usr/src

COPY pyproject.toml ./
COPY poetry.lock ./
RUN  pip install poetry && \
     poetry config virtualenvs.in-project true && \
     poetry install

FROM builder as test

ENV VIRTUAL_ENV=/usr/src/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . /usr/src
RUN FLASK_ENV=testing python -m pytest --cov=app --cov-branch --cov-fail-under=83 --cov-report term-missing -m unittest

FROM base as app

ENV VIRTUAL_ENV=/usr/src/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN groupadd -r scaffold && useradd --no-log-init -r -g scaffold scaffold

COPY --from=builder /usr/src/.venv/ /usr/src/.venv/
COPY . /usr/src
WORKDIR /usr/src

USER scaffold

ENTRYPOINT [ "/usr/bin/tini", "--" ]
