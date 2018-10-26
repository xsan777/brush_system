from django.test import TestCase
# from .models import *
import datetime

# Create your tests here.
now_time = datetime.datetime.now()
print(now_time)


def open_supplemental_data():
    def cheak_stats():
        now_time = datetime.datetime.now()

now_time = '2018-1-25'
# now_time = datetime.datetime.strptime(now_time,'%Y-%m-%d')
print(now_time)
def t_mouth_2(search_time):
    search_time = search_time.split('-')
    years = search_time[0]
    mouths = search_time[1]
    mouths = years + '-' +mouths + '-'
    return mouths
import time
now_time = time.strftime('%Y-%m-%d', now_time)
print(now_time)
print(t_mouth_2(str(now_time)))
