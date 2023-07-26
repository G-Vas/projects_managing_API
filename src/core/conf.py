from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASWORD = os.environ.get('DB_PASWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASWORD}@{DB_HOST}:5432/{DB_NAME}'
