from app import db


class Staycation(db.Document):
    meta = {'collection': 'staycation'}
    hotel_name = db.StringField()
    duration = db.IntField()
    unit_cost = db.FloatField()
    image_url = db.StringField()
    description = db.StringField()
