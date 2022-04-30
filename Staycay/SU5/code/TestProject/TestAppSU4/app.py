# import the Flask module and create an app using it
from flask import Flask
app = Flask(__name__)


# define the basic route '/'
# request handler for this route: display the following text
@app.route('/')
def main():
    return 'Hello World!'


# check if the executed file is the main program; if so, run the app
if __name__ == '__main__':
    app.run(debug=True)


