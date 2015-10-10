import datetime
from threading import Timer

import nest
from parse_rest.installation import Push
from parse_rest.connection import register
import requests
import RPi.GPIO as GPIO
import sendgrid

from models import History, Rules, Sensors
from sunset import get_sunset
from settings_local import APPLICATION_ID, REST_API_KEY, MASTER_KEY, username, password, SENDGRID_USERNAME, SENDGRID_PASSWORD

def window_opened(all_sensors, all_rules):
    window = True
    for sensor in all_sensors:
        if sensor.name == 'Window':
            sensor.open = True
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 2 and rule.is_enabled:
            # napi = nest.Nest(username, password)
            # for device in napi.devices:
            #     prev_nest_mode = device.mode
            #     device.mode = 'off'
            print 'Nest mode set to off and previous state stored.'

def window_closed(all_sensors, all_rules):
    window = False
    for sensor in all_sensors:
        if sensor.name == 'Window':
            sensor.open = False
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 2 and rule.is_enabled:
            # napi = nest.Nest(username, password)
            # for device in napi.devices:
            #     device.mode = prev_nest_mode
            print 'Mode restored to Nest.'

def garage_opened(all_sensors, all_rules):
    garage = True
    for sensor in all_sensors:
        if sensor.name == 'Garage':
            sensor.open = True
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 1 and rule.is_enabled:
            msg = 'You left a window open! Close it to avoid a security risk before leaving.'
            Push.message(msg, channels=["Notifications"])
            history_item = History(Text=msg)
            history_item.save()
            message = sendgrid.Mail(to='rohanmathur34@gmail.com', subject='Allstate Hub Notification', html='', text=msg, from_email='hub@allstate.com')
            status, mersg = sg.send(message)
        elif rule.rule_id == 3 and rule.is_enabled:
            # napi = nest.Nest(username, password)
            # for device in napi.devices:
            #     prev_nest_mode_garage = device.mode
            #     device.mode = 'off'
            print 'Nest mode set to off and previous state stored.'
        elif rule.rule_id == 4 and rule.is_enabled:
            msg = 'Make sure the alarm system is enabled!'
            Push.message(msg, channels=["Notifications"])
            history_item = History(Text=msg)
            history_item.save()
            message = sendgrid.Mail(to='rohanmathur34@gmail.com', subject='Allstate Hub Notification', html='', text=msg, from_email='hub@allstate.com')
            status, mersg = sg.send(message)

def garage_closed(all_sensors, all_rules):
    garage = False
    for sensor in all_sensors:
        if sensor.name == 'Garage':
            sensor.open = False
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 3 and rule.is_enabled:
            # napi = nest.Nest(username, password)
            # for device in napi.devices:
            #     device.mode = prev_nest_mode_garage
            print 'Mode restored to Nest.'

def smoke_on(all_sensors, all_rules):
    smoke = True
    GPIO.output(4, 1)
    for sensor in all_sensors:
        if sensor.name == 'Smoke':
            sensor.open = True
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 6 and rule.is_enabled:
            msg = 'Smoke alarm was triggered!'
            Push.message(msg, channels=["Notifications"])
            history_item = History(Text=msg)
            history_item.save()
            message = sendgrid.Mail(to='rohanmathur34@gmail.com', subject='Allstate Hub Notification', html='', text=msg, from_email='hub@allstate.com')
            status, mersg = sg.send(message)

def smoke_off(all_sensors, all_rules):
    smoke = False
    GPIO.output(4, 0)
    for sensor in all_sensors:
        if sensor.name == 'Smoke':
            sensor.open = False
            sensor.save()

def water_on(all_sensors, all_rules):
    water = True
    GPIO.output(3, 1)
    for sensor in all_sensors:
        if sensor.name == 'Water':
            sensor.open = True
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 6 and rule.is_enabled:
            msg = 'Flood detector was triggered!'
            Push.message(msg, channels=["Notifications"])
            history_item = History(Text=msg)
            history_item.save()
            message = sendgrid.Mail(to='rohanmathur34@gmail.com', subject='Allstate Hub Notification', html='', text=msg, from_email='hub@allstate.com')
            status, mersg = sg.send(message)

def water_off(all_sensors, all_rules):
    water = False
    GPIO.output(3, 0)
    for sensor in all_sensors:
        if sensor.name == 'Water':
            sensor.open = False
            sensor.save()

def fire_on(all_sensors, all_rules):
    fire = True
    GPIO.output(2, 1)
    for sensor in all_sensors:
        if sensor.name == 'Fire':
            sensor.open = True
            sensor.save()

    for rule in all_rules:
        if rule.rule_id == 6 and rule.is_enabled:
            msg = 'Fire alarm was triggered!'
            Push.message(msg, channels=["Notifications"])
            history_item = History(Text=msg)
            history_item.save()
            message = sendgrid.Mail(to='rohanmathur34@gmail.com', subject='Allstate Hub Notification', html='', text=msg, from_email='hub@allstate.com')
            status, mersg = sg.send(message)

def fire_off(all_sensors, all_rules):
    water = False
    GPIO.output(2, 0)
    for sensor in all_sensors:
        if sensor.name == 'Fire':
            sensor.open = False
            sensor.save()

window = False
garage = False
smoke = False
water = False
fire = False

prev_nest_mode = None
prev_nest_mode_garage = None

register(APPLICATION_ID, REST_API_KEY)
sg = sendgrid.SendGridClient('mathur', 'lolallstate222')
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

while(True):
    ret = requests.get('http://allstatehub.cfapps.io/data').content
    requests.delete('http://allstatehub.cfapps.io/data')

    if ret != '[]':
        if 'home.window.open' in ret:
            print 'Window opened'
        elif 'home.window.closed' in ret:
            print 'Window closed'
        elif 'home.garage.open' in ret:
            print 'Garage door opened'
        elif 'home.garage.closed' in ret:
            print 'Garage door closed'
        elif 'home.smoke.alarm_on' in ret:
            print 'Smoke alarm on'
        elif 'home.smoke.alarm_off' in ret:
            print 'Smoke alarm off'
        elif 'home.water.sensor.alarm_on' in ret:
            print 'Flood sensor detecting flooding'
        elif 'home.water.sensor.alarm_off' in ret:
            print 'Flood sensor off'
        elif 'home.fire.alarm_on' in ret:
            print 'Fire alarm off'
        elif 'home.fire.alarm_off' in ret:
            print 'Fire alarm on'

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
    elif 'home.fire.alarm_on' in ret:
        fire_on(all_sensors, all_rules)
    elif 'home.fire.alarm_off' in ret:
        fire_off(all_sensors, all_rules)

    for rule in all_rules:
        if rule.rule_id == 5 and rule.is_enabled:
            sunset_time = get_sunset()
            current_time = datetime.datetime.now().time()
            if sunset_time < current_time:
                # turn LEDs on
                pass