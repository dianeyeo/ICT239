from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson.son import SON
import json

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://<username>:<password>@cluster0-uftpg.mongodb.net/demo?retryWrites=true'
mongo = PyMongo(app)


@app.route('/')
def main():
    return 'Number of records: ' + str(mongo.db.news_mongo.count_documents({}))


# Deleting Information from Database
@app.route('/delete')
def delete():
    mongo.db.news_mongo.delete_many({})
    return 'Inserted: ' + str(mongo.db.news_mongo.count_documents({}))


# Adding Information to Database
@app.route('/add/<filename>')
def add(filename):
    # read content from the json file created earlier
    json_import = open(filename, 'r')
    partner_news = json.loads(json_import.read())
    mongo.db.news_mongo.insert_many(partner_news)
    return 'Inserted: ' + str(mongo.db.news_mongo.count_documents({}))


@app.route("/news")
def news():
    collection = mongo.db.news_mongo
    print('Count: ', collection.count_documents({}))
    pipeline = [
        {"$unwind": "$source"},
        {"$group": {"_id": "$source", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]
    records = list(collection.aggregate(pipeline))
    print('Records: ', records)
    # collection = [item for item in cursor]
    return render_template("index.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)