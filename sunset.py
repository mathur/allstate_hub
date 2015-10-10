import ast
import datetime

from flask import jsonify
import requests

def get_sunset():
    sunset_time = ast.literal_eval(requests.get('http://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400&date=today').content).get('results').get('sunset')
    sunset_time_split = sunset_time.split(':')
    sunset_time_split[2] = sunset_time_split[2][:2]
    time = datetime.time(sunset_time_split[0], sunset_time_split[1], sunset_time_split[2])
    return time

get_sunset()