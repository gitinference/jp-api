FROM --platform=$BUILDPLATFORM python:3.12 AS build

ARG TARGETPLATFORM
ARG BUILDPLATFORM

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 8000

COPY . .

# Create a script to run both commands
RUN printf '#!/bin/sh \n\
  python init.py && fastapi main.py --port 8000' > start.sh && \
  chmod +x start.sh

CMD ["./start.sh"]
