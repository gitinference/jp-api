FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 8000

COPY . .

CMD ["fastapi", "run", "main.py", "--port", "8000"]
