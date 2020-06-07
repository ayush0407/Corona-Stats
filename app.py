import codecs

import atexit
from flask import Flask,render_template
import urllib3
import requests
import csv
from flask_crontab import Crontab
import pandas as pd

app = Flask(__name__)
cron=Crontab(app)


class LocationsData:
    def __init__(self,state='NA',country='NA',latestCount=0,prevDayCount=0):
        self.state=state
        self.country=country
        self.latestCount=latestCount
        self.prevDayCount=prevDayCount
        #self.latestTotalCases=latestTotalCases
        #self.diffFromPrevDay=diffFromPrevDay

#* */1 * * * *



@cron.job(minute="/1")
@app.route('/')
def coronaStats():
    lis=[]
    url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

    response1=requests.get(url)
    file=open('C:\\Users\\ayush\\PycharmProjects\\Corona Tracker\\static\\response.csv',"w")
    file.write(response1.text)
    file.close()
    readResponse=open('C:\\Users\\ayush\\PycharmProjects\\Corona Tracker\\static\\response.csv','r')
    obj=csv.DictReader(readResponse)
    column_names=obj.fieldnames
    #print((column_names))
    for row in obj:
        diffFromPrevDay=int(row[column_names[-1]])-int(row[column_names[-2]])
        ld=LocationsData(row['Province/State'],row['Country/Region'],row[column_names[-1]],diffFromPrevDay)
        lis.append(ld)
    totalCount=0
    prevDayCount=0
    for data in lis:
        totalCount+=int(data.latestCount)
        prevDayCount+=data.prevDayCount












    return render_template('home.html',locationData=lis,tc=totalCount,pdc=prevDayCount)


if __name__ == '__main__':
    app.run()
