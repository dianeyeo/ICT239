# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

import io
import csv
# from dashboard import pCHART
from users import User
from staycation import Staycation
from book import Bookings
from flask_login import login_required, current_user
from flask import render_template, request
from app import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

# Register Blueprint so we can factor routes
from dashboard import dashboard
from auth import auth
from book_packages import product
from book_hotel import hotel
import users

# register blueprint from respective module
app.register_blueprint(dashboard)
app.register_blueprint(auth)
app.register_blueprint(product)
app.register_blueprint(hotel)


# Load the current user if any

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@app.route('/')
def show_base():
    return render_template('base.html')


@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        return render_template('products.html', name=current_user.name, panel='Package')


@ app.route('/upload', methods=['GET', 'POST'])
@ login_required
def upload():

    if request.method == 'GET':
        return render_template('upload.html', name=current_user.name, panel="Upload")

    elif request.method == 'POST':
        type = request.form.get('datatype')
        file = request.files.get('file')
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(
            data), delimiter=',', quotechar='"')
        file.close()
        print(type)

        for item in list(dict_reader):
            if type == 'users':
                hashpass = generate_password_hash(
                    item['password'], method='sha256')
                hey = User(
                    email=item['email'], password=hashpass, name=item['name']).save()
            elif type == 'staycation':
                stay = Staycation(
                    hotel_name=item['hotel_name'], duration=item['duration'],
                    unit_cost=item['unit_cost'], image_url=item['image_url'], description=item['description']).save()
            else:
                book = Bookings(
                    check_in_date=item['check_in_date'], customer=User, package=Staycation, total_cost=Bookings.calculate_total_cost(item)).save()

        return render_template("upload.html", name=current_user.name, panel="Upload")
