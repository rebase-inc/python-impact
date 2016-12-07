FROM alpine

COPY . /pyimpact

ARG PYPI_SERVER_HOST
ARG PYPI_SERVER_SCHEME
ARG PYPI_SERVER_PORT

RUN apk update && \
    apk add \
        --no-cache \
        ca-certificates \
        python3 && \
    pyvenv /venv && \
    source /venv/bin/activate && \
    python -m pip install --upgrade pip && \
    pip install \
        --no-cache-dir \
        --trusted-host ${PYPI_SERVER_HOST} \
        --extra-index-url ${PYPI_SERVER_SCHEME}${PYPI_SERVER_HOST}:${PYPI_SERVER_PORT} \
        --requirement /pyimpact/requirements.txt && \
    pip install wheel && \
    cd pyimpact && \
    python setup.py bdist_wheel --universal && \
    pip install --no-cache-dir --find-links dist dist/*
    
CMD ["/venv/bin/python", "-m", "pyimpact"]
