import os
import tempfile
from colocalization.model import load_data
import pytest
from flask import Flask
import tempfile


@pytest.fixture(scope='module')
def setup(request):
    print('\nresources_a_setup()')
    app = Flask(__name__, static_folder='static')
    app.testing = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    self.app = app.test_client()
    def teardown():
        print('\nresources_a_teardown()')
    request.addfinalizer(resource_a_teardown)

def test_load_data():
    path="test/data/data.csv"
    #load_data(path)
