# coding: utf-8
from datetime import datetime
from datetime import timedelta
import configparser
from bs4 import BeautifulSoup



def str2date(str_):
    '''
    format = YYYYMMDD
    '''
    data_date = datetime.strptime(str_, "%Y%m%d")
    return data_date

def htmlpage2dates(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')

    dates = []
            
    for i in soup.find_all('h3'):
        try:
            data_date = i.attrs["data-date"]
            data_date = str2date(data_date) 
            dates.append(data_date)
        except KeyError:
            pass
    return dates 

def get_dates_for_course(ini_loc='2301F2020.ini'):
    '''return all dates'''
    config = configparser.ConfigParser()

    config.read(ini_loc)

    start = str2date(config['dates']["start"])
    end = str2date(config["dates"]["end"])

    counter = start 
    delta = timedelta(days=1)

    MON = 0
    WED = 2
    FRI = 4
    dates_for_course = []

    while counter < end:
        if counter.weekday() in [MON, WED, FRI]:
            dates_for_course.append(counter)
            # counter.strftime("%A %Y-%m-%d")
        counter += delta 
    return dates_for_course


fn = "/tmp/a.html"
with open(fn, "r") as inf:
    dt = inf.read()

dates = htmlpage2dates(dt)

dates_for_course = get_dates_for_course()

for d in dates_for_course:
    print(d.strftime("%a %b %d"))