import abc
import csv
import typing
from flask_sqlalchemy import SQLAlchemy
import os
import json
from sqlalchemy import func, distinct
import gzip
from sqlalchemy.ext.hybrid import hybrid_property
from dataclasses import dataclass


@dataclass
class Colocalization(object):
    source1: str
    source2: str

    phenotype1: str
    phenotype1_description: str
    phenotype2: str
    phenotype2_description: str

    tissue1: str
    tissue2: str

    #def locus_id1(self):
    #    return "chr{chromosome}_{position}_{ref}_{alt}".format(chromosome=self.locus_id1_chromosome,
    #                                                           position=self.locus_id1_position,
    #                                                           ref=self.locus_id1_ref,
    #                                                           alt=self.locus_id1_alt)
    #
    #locus_id1_chromosome = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)
    #locus_id1_position = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)
    #locus_id1_ref = db.Column(db.String(1), unique=False, nullable=False, primary_key=True)
    #locus_id1_alt = db.Column(db.String(1), unique=False, nullable=False, primary_key=True)

    locus_id1: str
    locus_id2: str

    chromosome: int
    start: int
    stop: int

    clpp: float
    clpa: float
    beta_id1: float
    beta_id2: float

    variation: str
    vars_pip1: str
    vars_pip2: str
    vars_beta1: str
    vars_beta2: str
    len_cs1: int
    len_cs2: int
    len_inter: int


@dataclass
class PhenotypeSummary(object):
    None


@dataclass
class LocusSummary(object):
    None


class ColocalizationDAO(object):
    @abc.abstractmethod
    def get_phenotype_range_list(self,
                                 phenotype: str,
                                 chromosome: int,
                                 start: int,
                                 stop: int) -> typing.List[Colocalization]:
        return

    @abc.abstractmethod
    def get_phenotype_range_summary(self,
                                    phenotype: str,
                                    chromosome: int,
                                    start: int,
                                    stop: int) -> PhenotypeSummary:
        return

    @abc.abstractmethod
    def get_locus_summary(self,
                          locus: str) -> LocusSummary:
        return


db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/tmp.db')
SQLALCHEMY_TRACK_MODIFICATIONS = json.loads(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower())


class Colocalization(db.Model):

    source1 = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)
    source2 = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)

    phenotype1 = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)
    phenotype1_description = db.Column(db.String(80), unique=False, nullable=False)
    phenotype2 = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)
    phenotype2_description = db.Column(db.String(80), unique=False, nullable=False)

    tissue1 = db.Column(db.String(80), unique=False, nullable=True, primary_key=True)
    tissue2 = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)

    # locus_id1 data is split for search
    @hybrid_property
    def locus_id1(self):
        return "chr{chromosome}_{position}_{ref}_{alt}".format(chromosome=self.locus_id1_chromosome,
                                                               position=self.locus_id1_position,
                                                               ref=self.locus_id1_ref,
                                                               alt=self.locus_id1_alt)

    locus_id1_chromosome = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)
    locus_id1_position = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)
    locus_id1_ref = db.Column(db.String(1), unique=False, nullable=False, primary_key=True)
    locus_id1_alt = db.Column(db.String(1), unique=False, nullable=False, primary_key=True)


    locus_id2 = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)

    chromosome = db.Column(db.Integer, unique=False, nullable=False)
    start = db.Column(db.Integer, unique=False, nullable=False)
    stop = db.Column(db.Integer, unique=False, nullable=False)

    clpp = db.Column(db.Float, unique=False, nullable=False)
    clpa = db.Column(db.Float, unique=False, nullable=False)
    beta_id1 = db.Column(db.Float, unique=False, nullable=False)
    beta_id2 = db.Column(db.Float, unique=False, nullable=False)

    variation = db.Column(db.String(80), unique=False, nullable=False)
    vars_pip1 = db.Column(db.String(80), unique=False, nullable=False)
    vars_pip2 = db.Column(db.String(80), unique=False, nullable=False)
    vars_beta1 = db.Column(db.String(80), unique=False, nullable=False)
    vars_beta2 = db.Column(db.String(80), unique=False, nullable=False)
    len_cs1 = db.Column(db.Integer, unique=False, nullable=False)
    len_cs2 = db.Column(db.Integer, unique=False, nullable=False)
    len_inter = db.Column(db.Integer, unique=False, nullable=False)


    @staticmethod
    def column_names():
        return [ c.name for c in Colocalization.__table__.columns ]


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


def filter_min_cpla(min_clpa: typing.Optional[float]):
    filter_term = None
    if min_clpa:
        filter_term = [Colocalization.clpa >= min_clpa]
    else:
        filter_term = []
    return filter_term


def order_by_criterion(sort_by: typing.Optional[str],
                       desc: typing.Optional[bool]):
    column_name = Colocalization.column_names()

    if sort_by is not None and sort_by.lower() in column_name:
        column = getattr(Colocalization, sort_by)
        if desc:
            column = column.desc()
        else:
            column = column.asc()
        criterion = [column]
    else:
        criterion = []
    return criterion


def list_phenotype1(min_clpa: typing.Optional[float] = None,
                    desc=True):
    q = db.session.query(distinct(Colocalization.phenotype1))
    q = q.filter(*filter_min_cpla(min_clpa))
    phenotype1 = [r[0] for r in q.all()]
    return phenotype1


def load_data(path: str) -> None:
    with gzip.open(path, "rt") if path.endswith("gz") else open(path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter='\t', )
        expected_header = ["source1", "source2",
                           "pheno1", "pheno1_description",
                           "pheno2", "pheno2_description",
                           "tissue1", "tissue2",
                           "locus_id1", "locus_id2",
                           "chrom", "start", "stop",
                           "clpp", "clpa",
                           "beta_id1", "beta_id2",
                           "vars",
                           "vars_pip1", "vars_pip2",
                           "vars_beta1", "vars_beta2",
                           "len_cs1", "len_cs2", "len_inter"]
        actual_header = next(reader)
        count = 0
        assert expected_header == actual_header, "expected header '{expected_header}' got '{actual_header}'".format(expected_header=expected_header,
                                                                                                                    actual_header=actual_header)
        for line in reader:
            count = count + 1
            colocalization = csv_to_colocalization(line)
            db.session.add(colocalization)
            db.session.commit()
        return count


def load_phenotype1(path : str):
    db.session.query(Colocalization).delete(synchronize_session='evaluate')
    return load_data(path)


def row_to_dict(column_names):
    return lambda r: {c: getattr(r, c) for c in column_names}


def list_colocalization(phenotype1: str,
                        chromosome: int,
                        start: int,
                        stop: int,
                        min_clpa: typing.Optional[float] = None,
                        sort_by: typing.Optional[str] = None,
                        desc: bool = True):
    def query_filter(query):
        return query.filter(Colocalization.phenotype1 == phenotype1,
                            *filter_min_cpla(min_clpa))
    q = db.session.query(Colocalization)
    q = query_filter(q)
    q = q.order_by(*order_by_criterion(sort_by, desc))
    colocalizations = q.all()
    colocalizations = map(row_to_dict(Colocalization.column_names()),
                          colocalizations)
    colocalizations = list(colocalizations)
    return colocalizations


def summary_colocalization(phenotype1: str,
                           chromosome: int,
                           start: int,
                           stop: int,
                           min_clpa: typing.Optional[float] = None):
    def query_filter(query):
        return query.filter(Colocalization.phenotype1 == phenotype1,
                            *filter_min_cpla(min_clpa))
    count = query_filter(db.session.query(Colocalization)).count()
    unique_phenotype2 = query_filter(db.session.query(func.count(func.distinct(Colocalization.phenotype2)))).scalar()
    unique_tissue2 = query_filter(db.session.query(func.count(func.distinct(Colocalization.tissue2)))).scalar()
    result = {"count": count,
              "unique_phenotype2": unique_phenotype2,
              "unique_tissue2": unique_tissue2}
    return result


def locus_colocalization(phenotype1: str,
                         locus_id1: str,
                         min_clpa: typing.Optional[float] = None,
                         sort_by: typing.Optional[str] = "cpla",
                         desc: bool = True,
                         limit: typing.Optional[int] = 1):
    def query_filter(query):
        return query.filter(Colocalization.phenotype1 == phenotype1,
                            Colocalization.locus_id1 == locus_id1,
                            *filter_min_cpla(min_clpa))
    count = filter(db.session.query(Colocalization)).count()
    q = db.session.query(Colocalization)
    q = query_filter(q)
    q = q.order_by(*order_by_criterion(sort_by, desc))
    if limit is not None:
        q = q.limit(limit)
    colocalizations = q.all()
    colocalizations = map(row_to_dict(Colocalization.column_names()),
                          colocalizations)
    colocalizations = list(colocalizations)
    return {"count": count,
            "rows": colocalizations}


def csv_to_colocalization(line):
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
                                    beta_id1=nvl(line[15], float),
                                    beta_id2=nvl(line[16], float),

                                    variation=line[17],
                                    vars_pip1=line[18],
                                    vars_pip2=line[19],
                                    vars_beta1=line[20],
                                    vars_beta2=line[21],
                                    len_cs1=nvl(line[22], int),
                                    len_cs2=nvl(line[23], int),
                                    len_inter=nvl(line[24], int))
    return colocalization
