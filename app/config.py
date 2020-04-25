from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv('.env'))


class Config:
    ENV = os.getenv('ENV')
    DEV_DOMAIN = os.getenv('DEV_DOMAIN')
    DOMAIN = os.getenv('DOMAIN')
    PORT = int(os.getenv('PORT'))

    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = int(os.getenv('DB_PORT'))