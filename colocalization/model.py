import abc
import typing
import attr
from attr.validators import instance_of
from data_access.db import JSONifiable
import re

X = typing.TypeVar('X')


def _nvl(value: str, f: typing.Callable[[str], X]) -> typing.Optional[X]:
    """
    Wrapper to convert strings to a given type, where the
    empty string, or None is returned as None.

    :param value: string representing type X
    :param f: function from string to type X
    :return: X or None
    """
    if value is None:
        result = None
    elif value == "":
        result = None
    else:
        result = f(value)
    return result


@attr.s
class Colocalization(JSONifiable):
    """
    DTO for colocalization.

    https://github.com/FINNGEN/colocalization/blob/master/docs/data_dictionary.txt

    """
    source1 = attr.ib(validator=instance_of(str))
    source2 = attr.ib(validator=instance_of(str))
    phenotype1 = attr.ib(validator=instance_of(str))
    phenotype1_description = attr.ib(validator=instance_of(str))
    phenotype2 = attr.ib(validator=instance_of(str))
    phenotype2_description = attr.ib(validator=instance_of(str))
    tissue1 = attr.ib(validator=attr.validators.optional(instance_of(str)))
    tissue2 = attr.ib(validator=instance_of(str))
    locus_id1 = attr.ib(validator=instance_of(str))
    locus_id2 = attr.ib(validator=instance_of(str))
    chromosome = attr.ib(validator=instance_of(int))
    start = attr.ib(validator=instance_of(int))
    stop = attr.ib(validator=instance_of(int))
    clpp = attr.ib(validator=instance_of(float))
    clpa = attr.ib(validator=instance_of(float))
    beta_id1 = attr.ib(validator=instance_of(float))
    beta_id2 = attr.ib(validator=instance_of(float))
    variation = attr.ib(validator=instance_of(str))
    vars_pip1 = attr.ib(validator=instance_of(str))
    vars_pip2 = attr.ib(validator=instance_of(str))
    vars_beta1 = attr.ib(validator=instance_of(str))
    vars_beta2 = attr.ib(validator=instance_of(str))
    len_cs1 = attr.ib(validator=instance_of(int))
    len_cs2 = attr.ib(validator=instance_of(int))
    len_inter = attr.ib(validator=instance_of(int))

    def json_rep(self):
        return self.__dict__

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
        colocalization = Colocalization(source1=_nvl(line[0], str),
                                        source2=_nvl(line[1], str),

                                        phenotype1=_nvl(line[2], str),
                                        phenotype1_description=_nvl(line[3], str),
                                        phenotype2=_nvl(line[4], str),
                                        phenotype2_description=_nvl(line[5], str),

                                        tissue1=_nvl(line[6], str),
                                        tissue2=_nvl(line[7], str),
                                        locus_id1=_nvl(line[8], str),
                                        locus_id2=_nvl(line[9], str),

                                        chromosome=_nvl(line[10], int),
                                        start=_nvl(line[11], int),
                                        stop=_nvl(line[12], int),

                                        clpp=_nvl(line[13], float),
                                        clpa=_nvl(line[14], float),
                                        beta_id1=_nvl(line[15], float),
                                        beta_id2=_nvl(line[16], float),

                                        variation=_nvl(line[17], str),
                                        vars_pip1=_nvl(line[18], str),
                                        vars_pip2=_nvl(line[19], str),
                                        vars_beta1=_nvl(line[20], str),
                                        vars_beta2=_nvl(line[21], str),
                                        len_cs1=_nvl(line[22], int),
                                        len_cs2=_nvl(line[23], int),
                                        len_inter=_nvl(line[24], int))
        return colocalization


@attr.s
class SearchSummary(JSONifiable):
    """
    DTO containing a summary of colocalization records for a search.

    count: number of records found
    unique_phenotype2: the number of unique phenotypes found
    unique_tissue2: the number of unique tissues found
    """
    count = attr.ib(validator=instance_of(int))
    unique_phenotype2 = attr.ib(validator=instance_of(int))
    unique_tissue2 = attr.ib(validator=instance_of(int))

    def json_rep(self):
        return self.__dict__


@attr.s
class SearchResults(JSONifiable):
    """
    DTO containing the results of a search.

    count: number of records matched, note this may be different
           from the size of colocalization if a limit term
           is used.
    colocalization: list of colocalization matches
    """
    count = attr.ib(validator=instance_of(int))
    colocalizations = attr.ib(validator=attr.validators.deep_iterable(member_validator=instance_of(Colocalization),
                                                                      iterable_validator=instance_of(typing.List)))

    def json_rep(self):
        return self.__dict__


@attr.s
class ChromosomeRange(JSONifiable):
    """
        Chromosome coordinate range

        chromosome: chromosome
        start: start of range
        stop: end of range
    """
    chromosome = attr.ib(validator=instance_of(int))
    start = attr.ib(validator=instance_of(int))
    stop = attr.ib(validator=instance_of(int))

    @staticmethod
    def from_str(text: str) -> typing.Optional["ChromosomeRange"]:
        """
        Takes a string representing a range and returns a tuple of integers
        (chromosome,start,stop).  Returns None if it cannot be parsed.
        """
        fragments = re.match(r'(?P<chromosome>\d+):(?P<start>\d+)-(?P<stop>\d+)', text)
        if fragments is None:
            None
        else:
            return ChromosomeRange(chromosome=int(fragments.group('chromosome')),
                                   start=int(fragments.group('start')),
                                   stop=int(fragments.group('stop')))

    def to_str(self):
        """

        :return: string representation of range
        """
        return "{chromosome}:{start}-{stop}".format(chromosome=self.chromosome,
                                                    start=self.start,
                                                    stop=self.stop)

    def json_rep(self):
        return self.__dict__


class ColocalizationDAO:
    @abc.abstractmethod
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
