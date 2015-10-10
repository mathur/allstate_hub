from flask import Flask

from parse_rest.connection import register
import requests

from models import Sensors
from settings_local import APPLICATION_ID, REST_API_KEY, MASTER_KEY

app = Flask(__name__)

is_window_open = False

@app.route('/data')
def data():
    ret = requests.get('http://allstatehub.cfapps.io/data').content
    #requests.delete('http://allstatehub.cfapps.io/data')

    if 'home.window.open' in ret:
        window_opened()
    if 'home.window.closed' in ret:
        window_closed()

    all_sensors = Sensors.Query.all()
    print all_sensors

    return ret

def window_opened():
    is_window_open = True

def window_closed():
    is_window_open = False

if __name__ == '__main__':
    register(APPLICATION_ID, REST_API_KEY)
    app.run(debug=True)