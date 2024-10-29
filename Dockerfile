FROM python:3.12-slim
RUN apt update && apt install -y curl
WORKDIR /app/
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
RUN apt remove -y curl && rm -rf /var/cache/apt/archives /var/lib/apt/lists
COPY ./README.md ./pyproject.toml ./poetry.lock /app/
COPY ./src /app/src
ARG INSTALL_DEV=false
ENV INSTALL_DEV=$INSTALL_DEV
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --with dev --with api; else poetry install --with api; fi"
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]