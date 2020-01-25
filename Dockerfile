FROM kennethreitz/pipenv:latest AS build

ADD . /app
WORKDIR /app

RUN pipenv install --dev \
 && pipenv lock -r > requirements.txt \
 && pipenv run python setup.py bdist_wheel


FROM python:3.7-slim AS homework

COPY --from=build /app/dist/*.whl .
COPY --from=build /app/requirements.txt .

ARG DEBIAN_FRONTEND=noninteractive

RUN set -xe \
 && python3 -m pip install *.whl -r requirements.txt \
 && rm -f *.whl requirements.txt \
 && mkdir -p /app

USER daemon

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/waitress-serve", \
            "--listen", "0.0.0.0:8080", \
            "--connection-limit", "2000", \
            "--asyncore-use-poll", \
            "--call", "homework:create_app"]

ENV STARTUP_COALESCING_SECONDS=11

