from pytest import fixture

import easy_dict as nd


@fixture()
def n():
    return nd.NestedDict()


def test_set_pair_deep_keys_with_bracket(n):
    n['a'] = {}
    n['a']['b'] = {}
    n['a']['b']['c'] = 123
    n['d'] = None

    assert n == {'a': {'b': {'c': 123}}, 'd': None}
