# app.py

# import the Flask module and create an app using it
from flask import Flask
import json
app = Flask(__name__)

data = [
    {'id': '1', 'username': 'John', 'email': 'john@gmail.com'},
    {'id': '2', 'username': 'Mary', 'email': 'mary@gmail.com'},
    {'id': '3', 'username': 'Peter', 'email': 'peter@gmail.com'},
    {'id': '4', 'username': 'Ann', 'email': 'ann@gmail.com'},
]


# define the basic route '/'
@app.route('/')
@app.route('/student')
def main():
    return json.dumps(data)


# check if the executed file is the main program; if so, run the app
if __name__ == '__main__':
    app.run(debug=True)


