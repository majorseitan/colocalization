import typing
import click
from flask.cli import AppGroup, with_appcontext
from colocalization.model import db, load_data

data_cli = AppGroup('data')

@data_cli.command("init")
@with_appcontext
def init() -> None:
    db.create_all()


@data_cli.command("harness")
@with_appcontext
def harness() -> None:
    import pdb; pdb.set_trace()


@data_cli.command("load")
@click.argument("path")
@with_appcontext
def cli_load(path: str) -> None:
    load_data(path)
