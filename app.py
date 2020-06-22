import click
from colocation.model import data_cli, db, query, summary, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from flask import Flask, send_from_directory

import json
app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

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
def do_query():
    return json.dumps(query())


@app.route('/colocation/summary')
def do_summary():
    return json.dumps(summary())
