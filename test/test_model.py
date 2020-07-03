import os
import tempfile
from flask import Flask
import tempfile
from colocalization.model import _nvl


def test_nvl():
    assert _nvl(None, id) is None
    assert _nvl("", int) is None
    assert _nvl("1", int) == 1

