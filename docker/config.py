import os

CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
DB_URI = os.environ.get('DB_URI', '')
SQLALCHEMY_TRACK_MODIFICATIONS = False
CUSTOM_PATH = os.environ.get('CUSTOM_PATH', '/tmp/custom_reports/')
DEBUG = os.environ.get('PWB_DEBUG', 'false').lower() == 'true'
