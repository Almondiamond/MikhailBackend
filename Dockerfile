# Pull base image
FROM python:3.10.16-alpine3.21

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Copy project
COPY . .

# Копируем entrypoint.sh после основного COPY, чтобы он не затирался
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Указываем точку входа
ENTRYPOINT ["/entrypoint.sh"]
