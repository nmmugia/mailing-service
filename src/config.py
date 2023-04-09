import os

class Config(object):
    SECRET_KEY = '\xce\xcc\x9eV\x978\xafpbdO@J\x92\xcc\x80\xa8\xc5\xa0\xbbu&\x84\xba'
    
    DB_URL="localhost"
    DB_USERNAME = "postgres"
    DB_PASSWORD = "postgres"
    DB = "mailing"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql psycopg2://postgres:postgres@localhost:5432/mailing"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.mailtrap.io")
    MAIL_PORT = os.getenv("MAIL_PORT", 2525)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "e30df826374e12")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "29f63a4a03b3d3")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", True)
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", False)
