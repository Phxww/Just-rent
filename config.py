import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')or \
        'sqlite:///'+ os.path.join(basedir,'app.db')
    POSTS_PER_PAGE = 5
 
    # app.config['SECRET_KEY'] = SECRET_KEY