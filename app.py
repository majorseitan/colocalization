import typing
import click
from flask import Flask, send_from_directory, request
import logging
import json
import os
import tempfile
from werkzeug.utils import secure_filename
from colocalization.model import list_phenotype1, load_phenotype1, list_colocalization, summary_colocalization, locus_colocation
from colocalization.model import data_cli, db
from colocalization.model import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, list_phenotype1

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

upload_dir = tempfile.mkdtemp()

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


@app.route('/', methods=["GET"])
def root():
    return app.send_static_file('index.html')


@app.route('/static/js/<path:path>', methods=["GET"])
def send_js(path):
    return send_from_directory('static/static/js', path)


@app.route('/static/media/<path:path>', methods=["GET"])
def send_media(path):
    return send_from_directory('static/static/js', path)


@app.route('/static/css/<path:path>', methods=["GET"])
def send_css(path):
    return send_from_directory('static/static/css', path)


@app.route('/api/colocalization', methods=["GET"])
def get_phenotype1():
    return json.dumps(list_phenotype1(min_clpa=get_min_clpa(),
                                      desc=get_desc()))


@app.route('/api/colocalization', methods=["POST"])
def post_phenotype1():
    f = request.files['csv']
    path = secure_filename(f.filename)
    path = os.path.join(upload_dir, path)
    f.save(path)
    return json.dumps(load_phenotype1(path))


@app.route('/api/colocalization/<string:phenotype1>', methods=["GET"])
def get_colocalization(phenotype1: str):
    return json.dumps(list_colocalization(phenotype1,
                                          min_clpa = get_min_clpa(),
                                          sort_by = get_sort_by(),
                                          desc = get_desc()))


@app.route('/api/colocalization/<string:phenotype1>/summary', methods=["GET"])
def do_summary(phenotype1: str):
    return json.dumps(summary_colocalization(phenotype1,
                                             min_clpa = get_min_clpa()))

@app.route('/api/colocalization/<string:phenotype1>/locus_id/<string:locus_id1>', methods=["GET"])
def do_locus_colocation(phenotype1: str,locus_id1: str):
    return json.dumps(locus_colocation(phenotype1,
                                       locus_id1,
                                       min_clpa = get_min_clpa()))
