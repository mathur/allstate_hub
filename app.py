from flask import Flask

import nest
from parse_rest.installation import Push
from parse_rest.connection import register
import requests

from models import Rules, Sensors
from settings_local import APPLICATION_ID, REST_API_KEY, MASTER_KEY, username, password

app = Flask(__name__)

window = False
garage = False
smoke = False
water = False

prev_nest_mode = None
prev_nest_mode_garage = None

@app.route('/data')
def data():
    ret = requests.get('http://allstatehub.cfapps.io/data').content
    requests.delete('http://allstatehub.cfapps.io/data')

    all_sensors = Sensors.Query.all()
    all_rules = Rules.Query.all()

    if 'home.window.open' in ret:
        window_opened(all_sensors, all_rules)
    elif 'home.window.closed' in ret:
        window_closed(all_sensors, all_rules)
    elif 'home.garage.open' in ret:
        garage_opened(all_sensors, all_rules)
    elif 'home.garage.closed' in ret:
        garage_closed(all_sensors, all_rules)
    elif 'home.smoke.alarm_on' in ret:
        smoke_on(all_sensors, all_rules)
    elif 'home.smoke.alarm_off' in ret:
        smoke_off(all_sensors, all_rules)
    elif 'home.water.sensor.alarm_on' in ret:
        water_on(all_sensors, all_rules)
    elif 'home.water.sensor.alarm_off' in ret:
        water_off(all_sensors, all_rules)

    return ret

def window_opened(all_sensors, all_rules):
    window = True
    for sensor in all_sensors:
        if sensor.name == 'Window':
            sensor.open = True
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 2 and rule.is_enabled:
            napi = nest.Nest(username, password)
            for device in napi.devices:
                prev_nest_mode = device.mode
                device.mode = 'off'
            print 'Nest mode set to off and previous state stored.'

def window_closed(all_sensors, all_rules):
    window = False
    for sensor in all_sensors:
        if sensor.name == 'Window':
            sensor.open = False
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 2 and rule.is_enabled:
            napi = nest.Nest(username, password)
            for device in napi.devices:
                device.mode = prev_nest_mode
            print 'Mode restored to Nest.'

def garage_opened(all_sensors, all_rules):
    garage = True
    for sensor in all_sensors:
        if sensor.name == 'Garage':
            sensor.open = True
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 1 and rule.is_enabled:
            Push.message("You left a window open! Close it to avoid a security risk before leaving.", channels=["Notifications"])
        elif rule.rule_id == 3 and rule.is_enabled:
            napi = nest.Nest(username, password)
            for device in napi.devices:
                prev_nest_mode_garage = device.mode
                device.mode = 'off'
            print 'Nest mode set to off and previous state stored.'
        elif rule.rule_id == 4 and rule.is_enabled:
            Push.message("Make sure the alarm system is enabled!", channels=["Notifications"])

def garage_closed(all_sensors, all_rules):
    garage = False
    for sensor in all_sensors:
        if sensor.name == 'Garage':
            sensor.open = False
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 3 and rule.is_enabled:
            napi = nest.Nest(username, password)
            for device in napi.devices:
                device.mode = prev_nest_mode_garage
            print 'Mode restored to Nest.'

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