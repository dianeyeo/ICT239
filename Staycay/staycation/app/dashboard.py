from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io

from staycation import Staycation
from bookings import Bookings


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

        # for d in data:

        #     pDate = d['check_in_date']

        #     if pDate <= firstDate:
        #         firstDate = pDate

        #     if pDate >= lastDate:
        #         lastDate = pDate

        #     if readings.get(d['User']):
        #         readings[d['User']].append([d['check_in_date'], d['Income']])
        #     else:
        #         readings[d['User']] = [[d['check_in_date'], d['Income']]]

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


@dashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
def render_dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html', name=current_user.name, panel="Dashboard")

    elif request.method == 'POST':

        listOfPackage = []

        # TODO: dynamically get dates from file
        # don't hardcode the dates
        firstDate = datetime(2022, 1, 7)
        lastDate = datetime(2022, 3, 2)

        # delete all data from db
        # pCHART.objects(firstDate=firstDate, lastDate=lastDate).delete()

        # sort (inplace) check_in_date to get min & max for x-axis
        # check_in_date = Bookings.objects['check_in_date']
        # check_in_date.sort(key=lambda x: x.split('-')[0])

        # get data (check_in_date & hotel_name) from bookings.csv
        booking_records = Bookings.objects.all()

        # check_in_date, hotel_name
        check_in_date = request.args.get('check_in_date')
        hotel_name = request.args.get('hotel_name')

        for book in booking_records:
            check_in_date = book.check_in_date
            hotel_name = book.hotel_name
            # append selected data to list
            listOfPackage.append(
                {'check_in_date': check_in_date, 'hotel_name': hotel_name})

        # blank chart
        newChart = pCHART(firstDate=None, lastDate=None, readings=None).save()
        # populate blank chart with data from list
        newChart.insert_reading_data_into_database(listOfPackage)

        # # get objects from db
        pChartObjects = pCHART.objects(firstDate=firstDate, lastDate=lastDate)

        if len(pChartObjects) >= 1:
            readings = {}

            readings = pChartObjects[0]['readings']
            firstDate = pChartObjects[0]['firstDate']
            lastDate = pChartObjects[0]['lastDate']

            # get data
            chartData = {}
            chartLabels = []
            chartData, chartLabels = pChartObjects[0].prepare_chart_dimension_and_label(
            )
            return jsonify({'chartData': chartData, 'chartLabels': chartLabels})
