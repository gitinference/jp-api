import os

def read_secret_file(secret_path):
    with open(secret_path, 'r') as file:
        return file.read().strip()

def db_credentials():
    DB_USER = str(os.environ.get("POSTGRES_USER")).strip()
    DB_DB = str(os.environ.get("POSTGRES_DB")).strip()
    DB_PASSWORD = str(read_secret_file('/run/secrets/db-password')).strip()
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@database:5432/{DB_DB}"
    return DATABASE_URL
