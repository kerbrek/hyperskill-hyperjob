#################################################################
####################### BUILD STAGE #############################
#################################################################
FROM python:3.6-slim-buster as builder

RUN python -m pip install --no-cache-dir pipfile-requirements==0.3.0

WORKDIR /app

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY Pipfile.lock .
RUN pipfile2req > requirments.txt \
    && pip install --no-cache-dir -r requirments.txt

#################################################################
####################### TARGET STAGE ############################
#################################################################
FROM python:3.6-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN groupadd --system --gid 999 app \
    && useradd --system --uid 999 --gid app app \
    \
    && mkdir -p /app/static \
    && chown --recursive app:app /app
USER app

WORKDIR /app

COPY --chown=app:app --from=builder /app/venv /app/venv
COPY --chown=app:app . /app

ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--config", "./gunicorn.conf.py", "hyperjob.wsgi"]
