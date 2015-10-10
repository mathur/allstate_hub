from flask import Flask
import requests

app = Flask(__name__)

@app.route('/data')
def data():
    ret = requests.get('http://allstatehub.cfapps.io/data').content
    requests.delete('http://allstatehub.cfapps.io/data')

    return ret

if __name__ == '__main__':
    app.run(debug=True)