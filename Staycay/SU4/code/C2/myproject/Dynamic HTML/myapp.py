# Dynamic HTML Content
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/resource')
def resource():
    id = request.args.get('id')
    return render_template('main.html', template_id=id)

if __name__ == '__main__':
    app.run(debug=True)


