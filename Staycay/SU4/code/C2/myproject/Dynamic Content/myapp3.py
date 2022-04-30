# Dynamic HTML Page
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

# in flask, use request.args.get() to get the parameter value
@app.route('/resource')
def resource():
    id = request.args.get('id')
    return 'You typed ' + id

if __name__ == '__main__':
    app.run(debug=True)


