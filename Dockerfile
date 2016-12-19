FROM alpine

COPY ./requirements.txt /requirements.txt

RUN apk --quiet update && \
    apk --quiet add \
        --no-cache \
        ca-certificates \
        python3 && \
    pyvenv /venv/impact && \
    source /venv/impact/bin/activate && \
    pip install \
        --no-cache-dir \
        --requirement ./requirements.txt

WORKDIR /code

EXPOSE 25000

ENV LOG_LEVEL DEBUG

CMD ["/venv/impact/bin/python", "-m", "impact-python.server"]
