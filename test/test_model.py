import os
import tempfile
from flask import Flask
import tempfile
import uuid
import random
import pytest

from colocalization.model import _nvl, Colocalization, SearchSummary, SearchResults


def test_nvl():
    assert _nvl(None, id) is None
    assert _nvl("", int) is None
    assert _nvl("1", int) == 1


def test_colocalization():
    line = "source1,source2," \
           "phenotype1,phenotype1_description,phenotype2,phenotype2_description," \
           "tissue1,tissue2,locus_id1,locus_id2," \
           "1,2,3," \
           "4.0,5.0,6.0,7.0," \
           "variation,vars_pip1,vars_pip2,vars_beta1,vars_beta2," \
           "8,9,10"
    actual = Colocalization.from_list(line.split(","))
    expected = Colocalization(source1="source1", source2="source2",
                              phenotype1="phenotype1", phenotype1_description="phenotype1_description",
                              phenotype2="phenotype2", phenotype2_description="phenotype2_description",
                              tissue1="tissue1", tissue2="tissue2", locus_id1="locus_id1", locus_id2="locus_id2",
                              chromosome=1, start=2, stop=3,
                              clpp=4.0, clpa=5.0, beta_id1=6.0, beta_id2=7.0,
                              variation="variation",
                              vars_pip1="vars_pip1", vars_pip2="vars_pip2",
                              vars_beta1="vars_beta1", vars_beta2="vars_beta2",
                              len_cs1=8, len_cs2=9, len_inter=10)
    assert actual == expected
    reflection = Colocalization(**expected.json_rep())
    assert reflection == expected
    with pytest.raises(TypeError):
        Colocalization(source1="source1", source2="source2",
                       phenotype1="phenotype1", phenotype1_description="phenotype1_description",
                       phenotype2="phenotype2", phenotype2_description="phenotype2_description",
                       tissue1="tissue1", tissue2="tissue2", locus_id1="locus_id1", locus_id2="locus_id2",
                       chromosome=1, start=2, stop=3,
                       clpp=4.0, clpa=5.0, beta_id1=6.0, beta_id2=7.0,
                       variation="variation",
                       vars_pip1="vars_pip1", vars_pip2="vars_pip2",
                       vars_beta1="vars_beta1", vars_beta2="vars_beta2",
                       len_cs1=8, len_cs2=9, len_inter=None)


def test_search_summary():
    expected = {"count": random.randrange(100),
                "unique_phenotype2": random.randrange(100),
                "unique_tissue2": random.randrange(100)}
    actual = SearchSummary(**expected)
    assert expected == actual.json_rep()

    with pytest.raises(TypeError):
        SearchSummary(count=1,
                      unique_phenotype2="bad value",
                      unique_tissue2=None)


def test_search_results():
    expected = {"count": random.randrange(100),
                "colocalizations": []}
    actual = SearchResults(**expected)
    assert expected == actual.json_rep()
    with pytest.raises(TypeError):
        SearchResults(count=1,
                      colocalizations=None)
    with pytest.raises(TypeError):
        SearchResults(count=1,
                      colocalizations=[1])
