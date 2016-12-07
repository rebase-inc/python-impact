FROM alpine

COPY ./libs/pyimpact/requirements.txt /requirements.txt

ARG PYPI_SERVER_HOST
ARG PYPI_SERVER_SCHEME
ARG PYPI_SERVER_PORT

RUN apk update && \
    apk add \
        --no-cache \
        ca-certificates \
        python3 && \
    pyvenv /venv/impact && \
    source /venv/impact/bin/activate && \
    pip install \
        --no-cache-dir \
        --trusted-host ${PYPI_SERVER_HOST} \
        --extra-index-url ${PYPI_SERVER_SCHEME}${PYPI_SERVER_HOST}:${PYPI_SERVER_PORT} \
        --requirement ./requirements.txt

WORKDIR /pyimpact

CMD ["/venv/impact/bin/python", "-m", "libs.pyimpact.server"]
