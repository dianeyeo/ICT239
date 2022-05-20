from app import db
from users import User
from staycation import Staycation


# 'db.Document' is a document database (aka document oriented database) that stores information in documents
# Bookings class will have fields that are stored in db.Document
class Bookings(db.Document):
    # meta: also known as data of data
    # collection: a group of documents
    # ^ allows to store more than one document (i.e., more than 1 booking) in the same collection
    # give the collection a name; in this case, 'bookings'
    meta = {'collection': 'bookings'}
    # create a field for check in date
    # 'db.DateTimeField' : datatype for check in date to be stored as a datetime
    # 'required=True' : set the field of check in date to be required (MUST be filled in)
    check_in_date = db.DateTimeField(required=True)
    # create a field for customer
    # 'db.ReferenceField' : datatype for customer to be stored as a reference to User class
    # 'User' : set the field of customer to reference User class
    customer = db.ReferenceField(User)
    # create a field for package
    # 'db.ReferenceField' : datatype for package to be stored as a reference to Staycation class
    # 'Staycation' : set the field of package to reference Staycation class
    package = db.ReferenceField(Staycation)
    # create a field for total cost
    # 'db.FloatField' : datatype for total cost to be stored as a float
    total_cost = db.FloatField()

    # calculate the total cost of entire stay at hotel
    # total cost = duration * unit_cost
    def calculate_total_cost(self):
        # duration to retrieve from Staycation class
        # unit cost to retrieve from Staycation class
        self.total_cost = self.package.duration * self.package.unit_cost
