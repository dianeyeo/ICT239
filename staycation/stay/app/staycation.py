from app import db


# 'db.Document' is a document database (aka document oriented database) that stores information in documents
# Staycation class will have fields that are stored in db.Document
class Staycation(db.Document):
    # meta: also known as data of data
    # collection: a group of documents
    # ^ allows to store more than one document (i.e., more than 1 staycation) in the same collection
    # give the collection a name; in this case, 'staycation'
    meta = {'collection': 'staycation'}
    # create a field for hotel name
    # 'db.StringField' : datatype for hotel name to be stored as a string
    # 'max_length' : set the string field of hotel name to be a maximum of 30 characters
    hotel_name = db.StringField(max_length=30)
    # create a field for duration of stay at hotel
    # 'db.IntField' : datatype for duration to be stored as an integer
    duration = db.IntField()
    # create a field for unit cost of stay at hotel
    # 'unit_cost' : price of stay at hotel per night
    # 'db.FloatField' : datatype for unit cost to be stored as a float
    unit_cost = db.FloatField()
    # create a field for image url for hotel
    # 'db.StringField' : datatype for image url to be stored as a string
    # 'max_length' : set the string field of image url to be a maximum of 30 characters
    image_url = db.StringField(max_length=30)
    # create a field for description for hotel
    # 'db.StringField' : datatype for description to be stored as a string
    # 'max_length' : set the string field of description to be a maximum of 500 characters
    description = db.StringField(max_length=500)
