from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, redirect, render_template, url_for, flash
from forms import RegForm
from users import User

import csv

auth = Blueprint('auth', __name__)


# register using db (mongodb)
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(
                    form.password.data, method='sha256')
                hey = User(email=form.email.data, password=hashpass,
                           name=form.name.data).save()
                login_user(hey)
                # upon registration, redirects user to packages page
                return redirect(url_for('products'))
            else:
                form.email.errors.append("User already existed")
                render_template('register.html', form=form, panel="Register")

    return render_template('register.html', form=form, panel="Register")


# login using db (mongodb)
@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/')
def login():
    # if current_user.is_authenticated == True:
    #     return redirect(url_for('dashboard.render_dashboard'))
    form = RegForm()
    if request.method == 'POST':
        print(request.form.get('checkbox'))
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            # if user exists
            if check_user:
                # checks if user password matches password in db
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    # upon login, redirects user to packages page
                    return redirect(url_for('products'))
                else:
                    form.password.errors.append("User Password Not Correct")
            # user doesn't exist
            else:
                form.email.errors.append("No Such User")

    return render_template('login.html', form=form, panel="Login")


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
