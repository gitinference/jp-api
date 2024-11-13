import os

def read_secret_file(secret_path):
    with open(secret_path, 'r') as file:
        return file.read().strip()

def db_credentials():
    DB_USER = str(os.environ.get("POSTGRES_USER")).strip()
    DB_DB = str(os.environ.get("POSTGRES_DB")).strip()
    if os.environ.get("DEV") == "True":
        DB_PASSWORD = str(os.environ.get("POSTGRES_PASSWORD")).strip()
        HOST = "localhost"
    else:
        DB_PASSWORD = str(read_secret_file('/run/secrets/db-password')).strip()
        HOST = "database"
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:5432/{DB_DB}"
    return DATABASE_URL
