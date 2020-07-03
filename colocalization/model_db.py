import typing
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, String, Float, h
from colocalization.model import ColocalizationDAO, SearchSummary, ChromosomeRange, SearchResults
    #from sqlalchemy.ext.hybrid import hybrid_property

metadata = MetaData()
colocalization = Table('colocalization',
                       metadata,
                       Column('source1', String(80), unique=False, nullable=False, primary_key=True),
                       Column('source2', String(80), unique=False, nullable=False, primary_key=True),
                       Column('phenotype1', String(80), unique=False, nullable=False, primary_key=True),
                       Column('phenotype1_description', String(80), unique=False, nullable=False),
                       Column('phenotype2', String(80), unique=False, nullable=False, primary_key=True),
                       Column('phenotype2_description', String(80), unique=False, nullable=False),
                       Column('tissue1', String(80), unique=False, nullable=True, primary_key=True),
                       Column('tissue2', String(80), unique=False, nullable=False, primary_key=True),
                       # locus_id1 data is split for search

                       #@ hybrid_property
                       Column('locus_id1_chromosome', Integer, unique=False, nullable=False, primary_key=True),
                       Column('locus_id1_position', Integer, unique=False, nullable=False, primary_key=True),
                       Column('locus_id1_ref', String(1), unique=False, nullable=False, primary_key=True),
                       Column('locus_id1_alt', String(1), unique=False, nullable=False, primary_key=True),

                       Column('locus_id2', String(80), unique=False, nullable=False, primary_key=True),

                       Column('chromosome', Integer, unique=False, nullable=False),
                       Column('start', Integer, unique=False, nullable=False),
                       Column('stop', Integer, unique=False, nullable=False),

                       Column('clpp', Float, unique=False, nullable=False),
                       Column('clpa', Float, unique=False, nullable=False),
                       Column('beta_id1', Float, unique=False, nullable=False),
                       Column('beta_id2', Float, unique=False, nullable=False),

                       Column('variation', String(80), unique=False, nullable=False),
                       Column('vars_pip1', String(80), unique=False, nullable=False),
                       Column('vars_pip2', String(80), unique=False, nullable=False),
                       Column('vars_beta1', String(80), unique=False, nullable=False),
                       Column('vars_beta2', String(80), unique=False, nullable=False),
                       Column('len_cs1', Integer, unique=False, nullable=False),
                       Column('len_cs2', Integer, unique=False, nullable=False),
                       Column('len_inter', Integer, unique=False, nullable=False))



def locus_id1(self):
    return "chr{chromosome}_{position}_{ref}_{alt}".format(chromosome=self.locus_id1_chromosome,
                                                           position=self.locus_id1_position,
                                                           ref=self.locus_id1_ref,
                                                           alt=self.locus_id1_alt)




class ColocalizationDB(ColocalizationDAO):

    def __init__(self, db_url: str):
        engine = create_engine(db_url, echo=True)


    def get_phenotype_range(self,
                            phenotype: str,
                            chromosome_range: ChromosomeRange,
                            flags: typing.Dict[str, typing.Any]) -> SearchResults:
        """
        Search for colocalization that match
        phenotype and range and return them.

        :param phenotype: phenotype to match in search
        :param chromosome_range: chromosome range to search
        :param flags: a collection of optional flags

        :return: matching colocalizations
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_phenotype_range_summary(self,
                                    phenotype: str,
                                    chromosome_range: ChromosomeRange,
                                    flags: typing.Dict[str, typing.Any]) -> SearchSummary:
        """
        Search for colocalization that match
        phenotype and range a summary of matches.

        :param phenotype: phenotype to match in search
        :param chromosome_range: chromosome range to search
        :param flags: a collection of optional flags

        :return: summary of matching colocalizations
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_locus(self,
                  locus: str,
                  flags: typing.Dict[str, typing.Any]) -> SearchResults:
        raise NotImplementedError
