from flask import Flask

from parse_rest.connection import register
import requests

from models import Sensors
from settings_local import APPLICATION_ID, REST_API_KEY, MASTER_KEY

app = Flask(__name__)

window = False
garage = False
smoke = False
water = False

@app.route('/data')
def data():
    ret = requests.get('http://allstatehub.cfapps.io/data').content
    requests.delete('http://allstatehub.cfapps.io/data')

    all_sensors = Sensors.Query.all()

    if 'home.window.open' in ret:
        window_opened(all_sensors)
    elif 'home.window.closed' in ret:
        window_closed(all_sensors)
    elif 'home.garage.open' in ret:
        garage_opened(all_sensors)
    elif 'home.garage.closed' in ret:
        garage_closed(all_sensors)
    elif 'home.smoke.alarm_on' in ret:
        smoke_on(all_sensors)
    elif 'home.smoke.alarm_off' in ret:
        smoke_off(all_sensors)
    elif 'home.water.sensor.alarm_on' in ret:
        water_on(all_sensors)
    elif 'home.water.sensor.alarm_off' in ret:
        water_off(all_sensors)

    return ret

def window_opened(all_sensors):
    window = True
    for sensor in all_sensors:
        if sensor.name == 'window':
            sensor.open = True
            sensor.save()

def window_closed(all_sensors):
    window = False
    for sensor in all_sensors:
        if sensor.name == 'window':
            sensor.open = False
            sensor.save()

def garage_opened(all_sensors):
    garage = True
    for sensor in all_sensors:
        if sensor.name == 'garage':
            sensor.open = True
            sensor.save()

def garage_closed(all_sensors):
    garage = False
    for sensor in all_sensors:
        if sensor.name == 'garage':
            sensor.open = False
            sensor.save()

def smoke_on(all_sensors):
    smoke = True
    for sensor in all_sensors:
        if sensor.name == 'smoke':
            sensor.open = True
            sensor.save()

def smoke_off(all_sensors):
    smoke = False
    for sensor in all_sensors:
        if sensor.name == 'smoke':
            sensor.open = False
            sensor.save()

def water_on(all_sensors):
    water = True
    for sensor in all_sensors:
        if sensor.name == 'water':
            sensor.open = True
            sensor.save()

def water_off(all_sensors):
    water = False
    for sensor in all_sensors:
        if sensor.name == 'water':
            sensor.open = False
            sensor.save()

if __name__ == '__main__':
    register(APPLICATION_ID, REST_API_KEY)
    app.run(debug=True)