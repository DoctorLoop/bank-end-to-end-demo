"""Flask configuration variables."""
from os import environ, path
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(".env")

basedir = path.abspath(path.dirname(__file__))

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False