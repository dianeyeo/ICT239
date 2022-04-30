# import the Flask module and create an app using it
from flask import Flask, render_template
app = Flask(__name__)

data = [
    {'id': '1', 'username': 'John', 'email': 'john@gmail.com'},
    {'id': '2', 'username': 'Mary', 'email': 'mary@gmail.com'},
    {'id': '3', 'username': 'Peter', 'email': 'peter@gmail.com'},
    {'id': '4', 'username': 'Ann', 'email': 'ann@gmail.com'},
]


@app.route('/')
def main():
    return 'ICT239 T02 Website'


# Read
@app.route('/students')
def students():
    return render_template('index.html', data=data, title='My ICT239-T02 Title')


# check if the executed file is the main program; if so, run the app
if __name__ == '__main__':
    app.run(debug=True)


