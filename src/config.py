

import secrets

class Config:
    SECRET_KEY = secrets.token_urlsafe(32)
    print(SECRET_KEY)
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = '1234'
    MYSQL_DB = 'tienda_informatica'

config ={
    'development': DevelopmentConfig
}