import abc
import typing
import json

X = typing.TypeVar('X')


def _nvl(value: str, f: typing.Callable[[str], X]) -> typing.Optional[X]:
    """
    Wrapper to convert strings to a given type, where the
    empty string, or None is returned as None.

    :param value: string representing type X
    :param f: function from string to type X
    :return: X or None
    """
    result = None
    if value is None:
        result = None
    elif value == "":
        result = None
    else:
        result = f(value)
    return result


class Colocalization(object):
    """
    DTO for colocalization.  Implemented as such due to the lack
    of data classes.

    see : https://github.com/FINNGEN/colocalization/blob/master/docs/data_dictionary.txt

    """
    def __init__(self,
                 source1: str, source2: str,
                 phenotype1: str, phenotype1_description: str,
                 phenotype2: str, phenotype2_description: str,
                 tissue1: str, tissue2: str,
                 locus_id1: str, locus_id2: str,
                 chromosome: int, start: int, stop: int,
                 clpp: float, clpa: float, beta_id1: float, beta_id2: float,
                 variation: str,
                 vars_pip1: str, vars_pip2: str,
                 vars_beta1: str, vars_beta2: str,
                 len_cs1: int, len_cs2: int,
                 len_inter: int) -> None:
        self.source1 = source1
        self.source2 = source2

        self.phenotype1 = phenotype1
        self.phenotype1_description = phenotype1_description

        self.phenotype2 = phenotype2
        self.phenotype2_description = phenotype2_description

        self.tissue1 = tissue1
        self.tissue2 = tissue2

        self.locus_id1 = locus_id1
        self.locus_id2 = locus_id2

        self.chromosome = chromosome
        self.start = start
        self.stop = stop

        self.clpp = clpp
        self.clpa = clpa
        self.beta_id1 = beta_id1
        self.beta_id2 = beta_id2

        self.variation = variation
        self.vars_pip1 = vars_pip1
        self.vars_pip2 = vars_pip2
        self.vars_beta1 = vars_beta1
        self.vars_beta2 = vars_beta2
        self.len_cs1 = len_cs1
        self.len_cs2 = len_cs2
        self.len_inter = len_inter

    def to_dict(self) -> typing.Dict[str, any]:
        """
        Return a dictionary containing a representation
        of this object

        :return: dictionary
        """
        return {"source1": self.source1,
                "source2": self.source2,

                "phenotype1": self.phenotype1,
                "phenotype1_description": self.phenotype1_description,

                "phenotype2": self.phenotype2,
                "phenotype2_description": self.phenotype2_description,

                "tissue1": self.tissue1,
                "tissue2": self.tissue2,

                "locus_id1": self.locus_id1,
                "locus_id2": self.locus_id2,

                "chromosome": self.chromosome,
                "start": self.start,
                "stop": self.stop,

                "clpp": self.clpp,
                "clpa": self.clpa,
                "beta_id1": self.beta_id1,
                "beta_id2": self.beta_id2,

                "variation": self.variation,

                "vars_pip1": self.vars_pip1,
                "vars_pip2": self.vars_pip2,
                "vars_beta1": self.vars_beta1,
                "vars_beta2": self.vars_beta2,
                "len_cs1": self.len_cs1,
                "len_cs2": self.len_cs2,
                "len_inter": self.len_inter }

    @staticmethod
    def from_list(line: typing.List[str]) -> "Colocalization":
        """
        Constructor method used to create colocalization from
        a row of data.

        the order of the columns are:
        01..05 source1, source2, phenotype1, phenotype1_description, phenotype2
        06..10 phenotype2_description, tissue1, tissue2, locus_id1, locus_id2
        11..15 chromosome, start, stop, clpp, clpa
        16..20 beta_id1, beta_id2, variation, vars_pip1, vars_pip2
        21..25 vars_beta1, vars_beta2, len_cs1, len_cs2, len_inter

        :param line: string array with value
        :return: colocalization object
        """
        colocalization = Colocalization(source1=_nvl(line[0]),
                                        source2=_nvl(line[1]),

                                        phenotype1=_nvl(line[2]),
                                        phenotype1_description=_nvl(line[3]),
                                        phenotype2=_nvl(line[4]),
                                        phenotype2_description=_nvl(line[5]),

                                        tissue1=_nvl(line[6]),
                                        tissue2=_nvl(line[7]),
                                        locus_id1=_nvl(line[8]),
                                        locus_id2=_nvl(line[9]),

                                        chromosome=_nvl(line[10], int),
                                        start=_nvl(line[11], int),
                                        stop=_nvl(line[12], int),

                                        clpp=_nvl(line[13], float),
                                        clpa=_nvl(line[14], float),
                                        beta_id1=_nvl(line[15], float),
                                        beta_id2=_nvl(line[16], float),

                                        variation=line[17],
                                        vars_pip1=line[18],
                                        vars_pip2=line[19],
                                        vars_beta1=line[20],
                                        vars_beta2=line[21],
                                        len_cs1=_nvl(line[22], int),
                                        len_cs2=_nvl(line[23], int),
                                        len_inter=_nvl(line[24], int))
        return colocalization


class SearchSummary(object):
    def __init__(self,
                 count: int,
                 unique_phenotype2: int,
                 unique_tissue2: int) -> None:
        """
        A summary of colocalization records for a search.

        :param count: number of records found
        :param unique_phenotype2: the number of unique phenotypes found
        :param unique_tissue2: the number of unique tissues found
        """
        self.count = count
        self.unique_phenotype2 = unique_phenotype2
        self.unique_tissue2 = unique_tissue2

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        """
        Returns a dictionary representation of this object.

        :return: dictionary
        """
        {"count": self.count,
         "unique_phenotype2": self.unique_phenotype2,
         "unique_tissue2": self.unique_tissue2}


class SearchResults(object):
    """
    """
    def __init__(self,
                 count: int,
                 colocalization: typing.List[Colocalization]) -> None:
        self.count = count
        self.colocalization = colocalization

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        """
        Returns a dictionary representation of this object.

        :return: dictionary
        """
        {"count": self.count,
         "colocalization": self.colocalization}


class ColocalizationDAO(object):
    @abc.abstractmethod
    def get_phenotype_range(self,
                            phenotype: str,
                            chromosome: int,
                            start: int,
                            stop: int) -> SearchResults:
        return

    @abc.abstractmethod
    def get_phenotype_range_summary(self,
                                    phenotype: str,
                                    chromosome: int,
                                    start: int,
                                    stop: int) -> SearchSummary:
        return

    @abc.abstractmethod
    def get_locus(self,
                  locus: str) -> SearchResults:
        return
