from flask import Flask
import requests

app = Flask(__name__)

@app.route('/data')
def hello_world():
    return requests.get('http://allstatehub.cfapps.io/data').content

if __name__ == '__main__':
    app.run(debug=True)