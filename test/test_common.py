from colocalization.common import parse_range

def test_load_data():
    parse_range("12:442348-842348") == (12,442348,842348)
