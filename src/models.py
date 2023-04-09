from src import db
from enum import Enum

class QueueStatus(Enum):
    QUEUED = "QUEUED"
    FAILED = "FAILED"
    SENT = "SENT"

# Create an association table to connect Event and Recipient
event_recipient = db.Table('event_recipient',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('recipient_id', db.Integer, db.ForeignKey('recipients.id'), primary_key=True)
)

class Event(db.Model):
    """Model for Event"""

    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    emails = db.relationship('Email', backref='event', lazy=True)
    recipients = db.relationship('Recipient', secondary=event_recipient, backref=db.backref('events', lazy=True))

    def __init__(self, event_name):
        self.event_name = event_name

class Email(db.Model):
    """Model for emails."""

    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    email_subject = db.Column(db.String(255), nullable=False)
    email_content = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    queue_status = db.Column(db.Enum(QueueStatus), default=QueueStatus.QUEUED)
    queue_log = db.Column(db.Text)

    def __init__(self,
                event_id,
                email_subject,
                email_content,
                timestamp,
                queue_status = QueueStatus.QUEUED,
                queue_log = None
                ):
        self.event_id = event_id
        self.email_subject = email_subject
        self.email_content = email_content
        self.timestamp = timestamp
        self.queue_status = queue_status
        self.queue_log = queue_log

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'email_subject': self.email_subject,
            'email_content': self.email_content,
            'timestamp': self.timestamp.isoformat(),
            'queue_status': self.queue_status.value,
            'queue_log': self.queue_log,
        }

    def __repr__(self):
        return f'<Email subject {self.email_subject}>'


class Recipient(db.Model):
    """Model for recipients."""

    __tablename__ = 'recipients'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    # events = db.relationship('Event', secondary=event_recipient, backref=db.backref('recipients', lazy=True))
    

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f'<Email {self.email}>'

