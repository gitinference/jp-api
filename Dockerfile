FROM --platform=$BUILDPLATFORM python:3.12 AS build

ARG TARGETPLATFORM
ARG BUILDPLATFORM

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 8000

COPY ./src /app/

CMD ["fastapi", "run", "main.py", "--port", "8000"]
