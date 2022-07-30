FROM python:3.7-alpine
WORKDIR /flask_app
COPY . .
RUN \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt && \
 apk --purge del .build-deps

