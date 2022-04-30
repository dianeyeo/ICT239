from flask import request, render_template, Blueprint
from flask_login import login_required, current_user
from staycation import Staycation
from book_packages import product


hotel = Blueprint('hotel', __name__)


# book hotel from product page
@hotel.route('/book_hotel')
@login_required
def book_hotel_date():
    hotels = Staycation.objects.all()

    # get hotel name
    hotel_name = request.args.get('hotel_name')
    return render_template('book_hotel.html', name=current_user.name, panel=hotel_name, hotels=hotels)
