FROM python:3.11.2-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN mkdir /code
WORKDIR /code
ADD . .


RUN set -e; \
    /usr/local/bin/python -m pip install --upgrade pip ;\
    python -m pip install -r /code/requirements.txt ;\
    chmod +x /code/docker/entrypoints/entrypoint.sh ;

# Run the application
EXPOSE 8000
ENTRYPOINT ["/code/docker/entrypoints/entrypoint.sh"]
