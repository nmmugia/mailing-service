from marshmallow import Schema, fields


class SaveEmailsSchema(Schema):
    event_id = fields.Int(required=True)
    email_subject = fields.Str(required=True)
    email_content = fields.Str(required=True)
    timestamp = fields.DateTime(required=True)

class SaveRecipient(Schema):
    email = fields.Str(required=True)
    event_id = fields.Int(required=True)