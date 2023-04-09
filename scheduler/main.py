from flask import Flask
from celery import Celery
from src import db, create_app
from datetime import datetime
from src.models import Email, QueueStatus, Recipient, event_recipient
from flask_mail import Mail, Message
from src.config import Config

app = Flask(__name__)
mail = Mail(app)


celery = Celery('tasks', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
@celery.task(name='send_email')
def send_email(emails, subject, content):
    with app.app_context():
        msg = Message(recipients=emails, subject=subject, body=content, charset='UTF-8')
        mail.send(msg)
