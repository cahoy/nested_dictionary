from pytest import fixture

import easy_dict as nd


@fixture()
def n():
    return nd.NestedDict({'a': {'b': {'c': 123}}, 'd': {'e': 456}, 'f': {'e': 789}})


def test_get_with_chained_from_root(n):
    assert n['a']['b']['c'] == 123
    assert n == {'a': {'b': {'c': 123}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_get_with_chained_partial_keys(n):
    assert n['b']['c'] == 123
    assert n['c'] == 123
    assert n == {'a': {'b': {'c': 123}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_get_with_list_from_root(n):
    assert n[['a', 'b', 'c']] == 123
    assert n == {'a': {'b': {'c': 123}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_get_with_list_partial_keys(n):
    assert n[['b', 'c']] == 123
    assert n[['c']] == 123
    assert n == {'a': {'b': {'c': 123}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_get_with_slash_from_root(n):
    assert n['a/b/c'] == 123
    assert n == {'a': {'b': {'c': 123}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_get_with_slash_partial_keys(n):
    assert n['b/c'] == 123
    assert n['c'] == 123
    assert n == {'a': {'b': {'c': 123}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_get_multiple_keys(n):
    n['c'] = {'e': 123}
    assert sorted(n['e']) == [123, 456, 789]
    assert isinstance(n['e'], tuple)
