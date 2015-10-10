import ast

from flask import jsonify
import requests

def get_sunset():
    sunset_time = ast.literal_eval(requests.get('http://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400&date=today').content).get('results').get('sunset')
    return sunset_time