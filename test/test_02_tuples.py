from easy_dict import NestedDict as nd
from pytest import fixture, raises

@fixture()
def n():
    return nd.NestedDict()


# SETTING WITH TUPLE
def test_set_first_branch(n):
    n['a'] = None
    n[('a', 'b')] = None    # Value at 'a'
    n[('b', 'c')] = 123
    n['d'] = None

    assert n == {'a': {'b': {'c': 123}}, 'd': None}


def test_set_to_invalid_branch(n):
    n.clear()
    n['a'] = None
    with raises(KeyError):
        n[('non_exist_branch', 'b')] = None


def test_set_to_non_false_value(n):
    n.clear()
    n['a'] = 123
    with raises(ValueError):
        n[('a', 'b')] = None