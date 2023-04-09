import pytz
from datetime import datetime
from flask import Blueprint, jsonify, request
from src import db
from src.models import Email, Recipient, Event, event_recipient
from src.schema import SaveEmailsSchema, SaveRecipient
from unidecode import unidecode
from scheduler.main import send_email


app_blueprint = Blueprint("app_blueprint", __name__)

@app_blueprint.route("/save_emails", methods=["POST"])
def post_email():
    data = request.get_json()
    try:
        schema = SaveEmailsSchema()
        result = schema.load(data)
    except Exception as e:
        return {
            'message' : 'invalid input data. Check your data',
            'errors': e.messages
        }, 400
    email = Email(
        event_id=result["event_id"],
        email_subject=result["email_subject"],
        email_content=result["email_content"],
        timestamp=result["timestamp"],
    )
    recipient_emails = db.session.query(Recipient.email)\
        .join(event_recipient, Recipient.id == event_recipient.c.recipient_id)\
        .filter(event_recipient.c.event_id == result["event_id"])\
        .all()
    
    local_tz = pytz.timezone('Asia/Singapore')
    local_dt = local_tz.localize(result["timestamp"])
    send_email.apply_async(args=[recipient_emails, data['email_subject'], data['email_content'],], eta=local_dt.astimezone(pytz.utc))

    try:
        db.session.add(email)
        db.session.commit()
        return jsonify({"message": f"email with subject \"{email.email_subject}\" is successfully queued"}), 201
    except:
        return jsonify({"message": "failed creating email"}), 500

@app_blueprint.route('/emails', methods=['GET'])
def list_email():
    emails = db.session.query(Email).all()

    response = []
    for email in emails:
            response.append(email.to_dict())
        
    return {
        'message' : 'success get events',
        'data' : response
    }, 200

@app_blueprint.route('/event', methods=['POST'])
def save_event():
    data = request.json

    if data.get('event_name') == None:
        return {
            'message' : 'Error, event name is required'
        }, 400

    new_event = Event(
        event_name=data['event_name']
    )
    db.session.add(new_event)
    db.session.commit()

    return {
        'message' : 'success add event',
        'data' : data
    }, 201

@app_blueprint.route('/events', methods=['GET'])
def list_event():
    events = db.session.query(Event, Recipient.email)\
                  .outerjoin(event_recipient, Event.id == event_recipient.c.event_id)\
                  .outerjoin(Recipient, Recipient.id == event_recipient.c.recipient_id)\
                  .all()

    response = {}
    for event, recipient_email in events:
        if event.id in response:
            response[event.id]["recipient_emails"].append(recipient_email)
        else:
            response[event.id] = {
                'event_id': event.id,
                'event_name': event.event_name,
                'recipient_emails': [] if recipient_email is None else [recipient_email]
            }
        

    return {
        'message' : 'success get events',
        'data' : response
    }, 200

@app_blueprint.route('/recipient', methods=['POST'])
def save_recipient():
    data = request.get_json()
    try:
        schema = SaveRecipient()
        result = schema.load(data)
    except Exception as e:
        return {
            'message' : 'invalid input data. Check your data',
            'errors': e.messages
        }, 400
    try:
        recipient = db.session.query(Recipient).filter_by(email=result["email"]).one()
    except:
        recipient =  Recipient(
            email=unidecode(result['email'])
        )
    event = db.session.query(Event).filter_by(id=result['event_id']).one()
    event.recipients.append(recipient)
    db.session.add(recipient)
    db.session.commit()

    return {
        'message' : 'successfully add recipient',
        'data' : data
    }, 201

@app_blueprint.errorhandler(404)
def page_not_found(e) -> tuple:
    """
        Returning not found json on 404
    """
    return jsonify({'message': 'not found'}), 404