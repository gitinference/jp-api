FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
