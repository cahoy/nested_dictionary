from easy_dict import NestedDict as nd
from pytest import fixture, raises


@fixture()
def n():
    return nd.NestedDict()


def test_set_pair_deep_keys_with_bracket(n):
    n['a'] = {}
    n['a']['b'] = {}
    n['a']['b']['c'] = 123
    n['d'] = None

    assert n == {'a': {'b': {'c': 123}}, 'd': None}
