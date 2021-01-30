import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    """Set Flask config variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    
    SQLALCHEMY_DATABASE_URI = ('mssql://serverXX/XXXXX?driver=ODBC+Driver+13+for+SQL+Server?trusted_connection=yes') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
 
    DOWNLOAD_FOLDER = os.path.join(basedir, 'download')
    #ALLOWED_EXTENSIONS = {'pdf'}