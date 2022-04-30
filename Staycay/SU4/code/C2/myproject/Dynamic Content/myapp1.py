# Dynamic HTML Page
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

# a new route to handle request with data input from user
@app.route('/resource')
def resource():
    return 'text ICT239 T02 text'

if __name__ == '__main__':
    app.run(debug=True)


