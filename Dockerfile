FROM python:3.9-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /usr/src/app

COPY . the_od_bods

RUN mkdir -p jkan/_datasets

WORKDIR /usr/src/app/the_od_bods

RUN uv sync --no-dev

RUN chmod a+x run.sh

CMD ["uv", "run", "bash", "run.sh"]
