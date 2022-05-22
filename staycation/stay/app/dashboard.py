from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io

from staycation import Staycation
from book import Bookings
from users import User


dashboard = Blueprint('dashboard', __name__)


class pCHART(db.Document):
    # store data in mongodb
    meta = {'collection': 'chart'}
    firstDate = db.DateTimeField()
    lastDate = db.DateTimeField()
    readings = db.DictField()

    def get_dict_from_csv(self, file):
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(
            data), delimiter=',', quotechar='"')
        file.close()
        return(list(dict_reader))

    def insert_reading_data_into_database(self, data):
        readings = {}

        firstDate = datetime(2022, 1, 7)
        lastDate = datetime(2022, 3, 2)

        for d in data:

            pDate = d['check_in_date']

            if pDate <= firstDate:
                firstDate = pDate

            if pDate >= lastDate:
                lastDate = pDate

            if readings.get(d['User']):
                readings[d['User']].append([d['check_in_date'], d['Income']])
            else:
                readings[d['User']] = [[d['check_in_date'], d['Income']]]

        self.update(__raw__={'$set': {'readings': readings,
                    'firstDate': firstDate, 'lastDate': lastDate}})

    def prepare_chart_dimension_and_label(self):
        chartData = {}
        chartLabels = []

        start_date = self.firstDate
        end_date = self.lastDate
        step = timedelta(days=4)

        while start_date <= end_date:
            # months from 1 to 12
            month = str(start_date.month)
            day = str(start_date.day)
            year = str(start_date.year)

            pDateString = year + '-' + month + '-' + day
            chartLabels.append(pDateString)

            for key, values in self.readings.items():
                if not chartData.get(key):
                    chartData[key] = []

                filled = False

                for v in values:
                    pDate = v[0]

                    if pDate == start_date:
                        chartData[key].append(v[1])
                        filled = True
                    else:
                        if pDate > start_date:
                            if not filled:
                                chartData[key].append(-1)
                                break

            start_date += step

        return chartData, chartLabels


def calculate_hotelIncome():
    hotel_totalIncome = {}

    booking_records = Bookings.objects()

    for book in booking_records:
        # retrieve hotel name from staycation
        hotelName = book.package.hotel_name
        # store check_in_date in yyyy-mm-dd format
        check_in_date = book['check_in_date'].strftime('%Y-%m-%d')
        # retrieve total income from booking
        total_income = book.total_cost

        # if hotel name doesn't exist in hotel_totalIncome
        if hotelName not in hotel_totalIncome:
            hotel_totalIncome[hotelName] = {check_in_date: total_income}
        # if check_in_date exists >1 in hotel_totalIncome
        elif check_in_date in hotel_totalIncome[hotelName]:
            hotel_totalIncome[hotelName][check_in_date] += total_income
        # if check_in_date doesn't exist in hotel_totalIncome
        else:
            hotel_totalIncome[hotelName][check_in_date] = total_income

    return hotel_totalIncome


def chartDim(hotel_totalIncome, chartXLabels):
    hotelDim = hotel_totalIncome

    # for hotel in sortedHotelIncome:
    #     sortedHotelIncome[hotel] = {key: sortedHotelIncome[hotel][key]
    #                                 for key in sorted(sortedHotelIncome[hotel].keys())}
    #     sortedHotelIncome[hotel] = list(sortedHotelIncome[hotel].values())

    hotelDim = {}
    # access hotel names
    for hotel in hotel_totalIncome.keys():
        # give each value in range a deafult value of -1
        hotelDim[hotel] = [-1] * len(chartXLabels)

        # if date in chartXlabels not in hotel_totalIncome
        for date in hotel_totalIncome[hotel].keys():
            # identify index of date in chartXlabels, replace deafult value (-1) with total income
            hotelDim[hotel][chartXLabels.index(
                date)] = hotel_totalIncome[hotel][date]

    return hotelDim


def chartXLabels():
    booking_dates = Bookings.objects().distinct('check_in_date')
    booking_dates = [i.strftime('%Y-%m-%d') for i in booking_dates]
    return booking_dates


def userChartLabels():
    hotels_stayed = Bookings.objects().distinct('package.hotel_name')
    user_booking = Bookings.objects().distinct('user')


def calculate_total_due(due, target):
    bookings_due = {}
    bookings = Bookings.objects().all()

    for book in bookings:
        if due == 'hotel':
            if book.package.hotel_name == target:
                if book.customer.name in bookings_due:
                    bookings_due[book.customer.name] += 1
                else:
                    bookings_due[book.customer.name] = 1
        else:
            if book.customer.name == target:
                print(book.customer.name)
                if book.package.hotel_name in bookings_due:
                    bookings_due[book.package.hotel_name] += 1
                else:
                    bookings_due[book.package.hotel_name] = 1

    return bookings_due


# Dashboard: Total Income Chart
@dashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
def render_dashboard():
    if request.method == 'GET':
        return render_template('trend_chart.html', name=current_user.name, panel="Dashboard")

    elif request.method == 'POST':

        hotelTotalIncome = calculate_hotelIncome()
        chartLabels = chartXLabels()
        chartData = chartDim(hotelTotalIncome, chartLabels)

        return jsonify({'chartData': chartData, 'chartLabels': chartLabels})


# Dashboard: Due Per User Chart
@dashboard.route('/dashboard_due_per_user', methods=['GET', 'POST'])
@login_required
def due_per_user():
    users = User.objects().all()
    userList = [user.name for user in users]
    target = request.form.get('user_due')
    # check
    print(target)

    if request.method == 'GET':
        return render_template('bar_chart.html', panel='Dashboard', userList=userList)

    elif request.method == 'POST':

        user_due = calculate_total_due('user', userList)
        # userChartLabel = userChartLabels()
        # chartData = chartDim(user_due, userChartLabel)

        return jsonify({'user_due': 'user_due', 'userChartLabel': 'hi'})


# Dashboard: Due Per Hotel Chart
@dashboard.route('/dashboard_due_per_hotel', methods=['GET', 'POST'])
@login_required
def due_per_hotel():
    hotels = Staycation.objects.all()
    hotelList = [hotel.hotel_name for hotel in hotels]
    target = request.form.get('hotel_due')
    # check
    print(target)

    if request.method == 'GET':
        return render_template('bar_chart.html', panel='Dashboard', hotelList=hotelList)

    elif request.method == 'POST':

        hotel_due = calculate_total_due('hotel', hotelList)

        return jsonify({'hotel_due': hotel_due, 'userChartLabel': 'hi'})


# function to post data that is selected at sidebar
def getUserData():
    user = request.path.get('user_due')
    return user
