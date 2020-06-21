import click
import csv
import typing
from flask.cli import AppGroup, with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
data_cli = AppGroup('data')

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False


class Colocalization(db.Model):
    # need to put a real id
    id = db.Column(db.Integer, unique=True, primary_key=True)
    source1 = db.Column(db.String(80), unique=False, nullable=False)  # , primary_key=True)
    source2 = db.Column(db.String(80), unique=False, nullable=False)  # , primary_key=True)

    phenotype1 = db.Column(db.String(80), unique=False, nullable=False)  # , primary_key=True)
    phenotype1_description = db.Column(db.String(80), unique=False, nullable=False)
    phenotype2 = db.Column(db.String(80), unique=False, nullable=False)  # , primary_key=True)
    phenotype2_description = db.Column(db.String(80), unique=False, nullable=False)

    tissue1 = db.Column(db.String(80), unique=False, nullable=True)
    tissue2 = db.Column(db.String(80), unique=False, nullable=False)
    locus_id1 = db.Column(db.String(80), unique=False, nullable=False)  # , primary_key=True)
    locus_id2 = db.Column(db.String(80), unique=False, nullable=False)  # , primary_key=True)

    chromosome = db.Column(db.Integer, unique=False, nullable=False)
    start = db.Column(db.Integer, unique=False, nullable=False)
    stop = db.Column(db.Integer, unique=False, nullable=False)

    clpp = db.Column(db.Float, unique=False, nullable=False)
    clpa = db.Column(db.Float, unique=False, nullable=False)
    beta_id1 = db.Column(db.Float, unique=False, nullable=True)  # Checked
    beta_id2 = db.Column(db.Float, unique=False, nullable=False)

    variation = db.Column(db.String(80), unique=False, nullable=False)
    vars_pip1 = db.Column(db.String(80), unique=False, nullable=False)
    vars_pip2 = db.Column(db.String(80), unique=False, nullable=False)
    vars_beta1 = db.Column(db.String(80), unique=False, nullable=False)
    vars_beta2 = db.Column(db.String(80), unique=False, nullable=False)
    len_cs1 = db.Column(db.Integer, unique=False, nullable=False)
    len_cs2 = db.Column(db.Integer, unique=False, nullable=False)
    len_inter = db.Column(db.Integer, unique=False, nullable=False)


@data_cli.command("init")
@with_appcontext
def load_data() -> None:
    db.create_all()


X = typing.TypeVar('X')


def nvl(value: str, f=str) -> typing.Optional[X]:
    result = None
    if value is None:
        result = None
    elif value == "":
        result = None
    else:
        result = f(value)
    return result


def fetch_all():
    colocalizations = db.session.query(Colocalization).all()
    colocalizations = map(lambda c: {k: v for k, v in vars(c).items() if not k.startswith('_')}, colocalizations)
    colocalizations = list(colocalizations)
    return colocalizations

@data_cli.command("load")
@click.argument("path")
@with_appcontext
def load_data(path: str) -> None:
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter='\t', )
        next(reader)
        for line in reader:
            colocalization = Colocalization(source1=nvl(line[0]),
                                            source2=nvl(line[1]),

                                            phenotype1=nvl(line[2]),
                                            phenotype1_description=nvl(line[3]),
                                            phenotype2=nvl(line[4]),
                                            phenotype2_description=nvl(line[5]),

                                            tissue1=nvl(line[6]),
                                            tissue2=nvl(line[7]),
                                            locus_id1=nvl(line[8]),
                                            locus_id2=nvl(line[9]),

                                            chromosome=nvl(line[10], int),
                                            start=nvl(line[11], int),
                                            stop=nvl(line[12], int),

                                            clpp=nvl(line[13], float),
                                            clpa=nvl(line[14], float),
                                            beta_id2=line[16],

                                            variation=line[17],
                                            vars_pip1=line[18],
                                            vars_pip2=line[19],
                                            vars_beta1=line[20],
                                            vars_beta2=line[21],
                                            len_cs1=nvl(line[22], int),
                                            len_cs2=nvl(line[23], int),
                                            len_inter=nvl(line[24], int))
            db.session.add(colocalization)
            db.session.commit()
