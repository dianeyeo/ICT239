from app import db


class Bookings(db.Document):
    meta = {'collection': 'bookings'}
    check_in_date = db.DateTimeField()
    customer = db.StringField()
    hotel_name = db.StringField()
