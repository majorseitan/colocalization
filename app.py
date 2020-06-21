import click
from colocation.data import data_cli, db, fetch_all
from flask import Flask, send_from_directory

import json
app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.cli.add_command(data_cli)
db.init_app(app)


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/static/js', path)


@app.route('/static/media/<path:path>')
def send_media(path):
    return send_from_directory('static/static/js', path)


@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/static/css', path)

@app.route('/colocation')
def data():
    return json.dumps(fetch_all())
