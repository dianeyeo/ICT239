# import the Flask module and create an app using it
# pip install flask_pymongo
# pip install dnspython
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
# ObjectId: properly obtain the value of the mongoDB _id field
from bson.objectid import ObjectId
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://<Username>:<Password>@cluster0-uftpg.mongodb.net/test?retryWrites=true'
# app.config['MONGO_DBNAME'] = 'test' # already specified in URI
mongo = PyMongo(app)


@app.route('/')
def main():
    # we are getting data from the mongodb collection - student
    cursor = mongo.db.student.find()
    # the count() method returns the number of record in the
    record_count = str(cursor.count())
    return 'Number of records: ' + record_count


@app.route('/students')
def students():
    cursor = mongo.db.student.find()
    new_list = [item for item in cursor]
    return render_template('index.html', data=new_list)


# Adding Information to Database
@app.route('/students/add', methods=['POST', 'GET'])
def add():
    # POST: processes the data and inserts the values into the MongoDB
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        # insert(): insert new records to a MongoDB collection
        # JSON format key-values
        mongo.db.student.insert({'username':name,'email':email})
    # GET (default): renders a form with the necessary input fields
    return render_template('form.html')


# Delete Information from Database
@app.route('/students/delete_name/<username>')
def delete_name(username):
    mongo.db.student.delete_one({'username': username})
    return 'No such user using delete_name'


# possible multiple items with the same username
# as _id is unique, using this is more precise
# _id is saved as a bson (binary JSON) objectId
@app.route('/students/delete_id/<idx>')
def delete_id(idx):
    # ObjectId: properly obtain the value of the mongoDB _id field
    mongo.db.student.delete_one({'_id': ObjectId(idx)})
    return 'No such user using delete_id'


# check if the executed file is the main program; if so, run the app
if __name__ == '__main__':
    app.run(debug=True)


