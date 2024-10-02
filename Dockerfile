FROM python:3.11.9-slim-bullseye AS base
RUN apt-get update && apt-get install curl -y
RUN export POETRY_HOME=/usr/local; curl -sSL https://install.python-poetry.org | python3.11 -
EXPOSE 8000
WORKDIR /opt/todoapp
COPY ["poetry.lock", "poetry.toml", "pyproject.toml", "./"]
RUN poetry install --no-dev --no-root

FROM base AS development
ENV FLASK_DEBUG="true"
RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base AS debug
ENV FLASK_DEBUG="true"
RUN poetry install
ENTRYPOINT tail -f /dev/null

FROM base AS production
RUN poetry install --no-dev
COPY ./todo_app ./todo_app
ENTRYPOINT poetry run gunicorn --bind 0.0.0.0 'todo_app.app:create_app()'

FROM base AS e2e_test_base
ENV FLASK_DEBUG="true"
RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN poetry install
COPY .env.test ./

FROM e2e_test_base AS local_tests
ENTRYPOINT ["poetry", "run", "pytest"]

FROM base AS watch_unit_tests
ENV FLASK_DEBUG="true"
RUN poetry install
COPY .env.test ./
ENTRYPOINT ["poetry", "run", "ptw", "--runner", "poetry run pytest", "--poll"]

FROM base AS pipeline_integration_tests
ENV FLASK_DEBUG="true"
RUN poetry install
COPY .env.test ./
COPY ./tests ./tests
COPY ./todo_app ./todo_app
ENTRYPOINT ["poetry", "run", "pytest"]

FROM e2e_test_base AS pipeline_e2e_tests
COPY ./e2eTests ./e2eTests
COPY ./todo_app ./todo_app
ENTRYPOINT ["poetry", "run", "pytest"]
