import typing
import click
from colocation.model import data_cli, db, query, summary, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, list_phenotype1
from flask import Flask, send_from_directory, request

import json
app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

app.cli.add_command(data_cli)
db.init_app(app)


def get_min_clpa() -> typing.Optional[float]:
    return request.args.get('min_clpa')

def get_sort_by() -> typing.Optional[str]:
    return request.args.get('sort_by')

def get_desc() -> bool:
    order_by = request.args.get('order_by')
    if order_by == 'desc':
        desc = True
    elif order_by == 'asc':
        desc = False
    else:
        desc = True
    return desc


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


@app.route('/phenotype1')
def do_list_phenotype1():
    return json.dumps(list_phenotype1(min_clpa=get_min_clpa(),
                                      desc=get_desc()))

@app.route('/colocation/<string:phenotype1>')
def do_query(phenotype1):
    return json.dumps(query(phenotype1,
                            min_clpa = get_min_clpa(),
                            sort_by = get_sort_by(),
                            desc = get_desc()))


@app.route('/colocation/<string:phenotype1>/summary')
def do_summary(phenotype1):
    return json.dumps(summary(phenotype1,
                              min_clpa = get_min_clpa()))
