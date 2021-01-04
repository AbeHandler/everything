from setops import cardinality
from setops import times_three


def test_times_three():
    assert times_three(3) == 9


def test_cardinality():
    assert cardinality({"dog", "cat", "bird"}) == 3
