from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from staycation import Staycation
import csv


product = Blueprint('product', __name__)


# render product page - reads from csv file
@product.route('/products')
@login_required
def book_package():
    # read staycation.csv file
    with open('assets/js/staycation.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        packages = list(reader)
        # print(packages)
        return render_template('products.html', name=current_user.name, panel="Package", products=packages)


# # render product page - reads from db(monogodb)
# @product.route('/products')
# @login_required
# def book_package():
#     packages = Staycation.objects.all()
#     return render_template('products.html', name=current_user.name, panel='Package', products=packages)
