from app import db
from flask_login import UserMixin


# Create a User class that inherits from the UserMixin class
# 'UserMixin' class provides default implementations for the methods that Flask-Login expects user objects to have
# 'db.Document' is a document database (aka document oriented database) that stores information in documents
# User class will have fields that are stored in db.Document
class User(UserMixin, db.Document):
    # meta: also known as data of data
    # collection: a group of documents
    # ^ allows to store more than one document (i.e., more than 1 user) in the same collection
    # give the collection a name; in this case, 'appUsers'
    meta = {'collection': 'appUsers'}
    # create a field for users' email
    # 'db.StringField' : datatype for user email to be stored as a string
    # 'max_length' : set the string field of user email to be a maximum of 30 characters
    email = db.StringField(max_length=30)
    # create a field for users' password
    # 'db.StringField' : datatype for user password to be stored as a string
    password = db.StringField()
    # create a field for users' name
    # 'db.StringField' : datatype for user name to be stored as a string
    name = db.StringField()
