ARG PYTHON_VERSION=3.12.3-bullseye

FROM python:${PYTHON_VERSION} AS python


FROM python AS python-build-stage
ARG BUILD_ENVIRONMENT=prod

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt


FROM python AS python-run-stage
ARG BUILD_ENVIRONMENT=prod

ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV ${BUILD_ENVIRONMENT}

ENV DJANGO_ENVIRONMENT ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN addgroup --system django && \
    adduser --system --ingroup django dajngo && \
    mkdir -p ${APP_HOME}/staticfiles && \
    mkdir -p ${APP_HOME}/mediafiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/mediafiles && \
    chmod 775 ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/mediafiles

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext netcat \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/list/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    rm -rf /wheels/

COPY --chown=django:django ./docker/prod/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=django:django ./docker/prod/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY --chown=django:django ./docker/prod/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/prod/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

COPY --chown=django:django ./src ${APP_HOME}

USER django

ENTRYPOINT [ "/entrypoint" ]