

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}