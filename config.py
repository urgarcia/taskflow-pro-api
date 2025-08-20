import os

from extensions import db, jwt

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'thiSsdn34_?1nds_!=2QWex')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "mysql+pymysql://root:root@localhost:3306/dish_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False