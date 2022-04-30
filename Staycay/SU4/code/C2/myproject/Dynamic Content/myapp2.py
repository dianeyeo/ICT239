# Dynamic HTML Page
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

# to be able to handle user input as part of the url
@app.route('/resource/<id>')
def resource(id):
    return 'You typed ' + id

if __name__ == '__main__':
    app.run(debug=True)


