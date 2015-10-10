from flask import Flask

from parse_rest.installation import Push
from parse_rest.connection import register
import requests

from models import Rules, Sensors
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
    all_rules = Rules.Query.all()

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

def window_opened(all_sensors, all_rules):
    window = True
    for sensor in all_sensors:
        if sensor.name == 'Window':
            sensor.open = True
            sensor.save()

def window_closed(all_sensors, all_rules):
    window = False
    for sensor in all_sensors:
        if sensor.name == 'Window':
            sensor.open = False
            sensor.save()

def garage_opened(all_sensors, all_rules):
    garage = True
    for sensor in all_sensors:
        if sensor.name == 'Garage':
            sensor.open = True
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 1 && rule.enabled == True:
            Push.message("You left a window open! Close it to avoid a security risk before leaving.", channels=["Notifications"])

def garage_closed(all_sensors, all_rules):
    garage = False
    for sensor in all_sensors:
        if sensor.name == 'Garage':
            sensor.open = False
            sensor.save()

def smoke_on(all_sensors, all_rules):
    smoke = True
    for sensor in all_sensors:
        if sensor.name == 'Smoke':
            sensor.open = True
            sensor.save()

def smoke_off(all_sensors, all_rules):
    smoke = False
    for sensor in all_sensors:
        if sensor.name == 'Smoke':
            sensor.open = False
            sensor.save()

def water_on(all_sensors, all_rules):
    water = True
    for sensor in all_sensors:
        if sensor.name == 'Water':
            sensor.open = True
            sensor.save()

def water_off(all_sensors, all_rules):
    water = False
    for sensor in all_sensors:
        if sensor.name == 'Water':
            sensor.open = False
            sensor.save()

if __name__ == '__main__':
    register(APPLICATION_ID, REST_API_KEY)
    app.run(debug=True)