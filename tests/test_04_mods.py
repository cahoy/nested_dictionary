from pytest import fixture, raises

import easy_dict as nd


@fixture()
def n():
    return nd.NestedDict({'a': {'b': {'c': 123}}, 'd': {'e': 456}, 'f': {'e': 789}})


def test_mod_rooted_chain(n):
    n['a']['b']['c'] = 234
    assert n == {'a': {'b': {'c': 234}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_mod_floating_chain(n):
    n['b']['c'] = 345
    assert n == {'a': {'b': {'c': 345}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_mod_floating_single_key(n):
    n['c'] = 456
    assert n == {'a': {'b': {'c': 456}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_mod_with_rooted_slash(n):
    n['a/b/c'] = 567
    assert n == {'a': {'b': {'c': 567}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_mod_with_floating_slash(n):
    n['b/c'] = 678
    assert n == {'a': {'b': {'c': 678}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_mod_with_floating_list(n):
    n[['b', 'c']] = 789
    assert n == {'a': {'b': {'c': 789}}, 'd': {'e': 456}, 'f': {'e': 789}}


def test_mod_multiple_keys_multi_target(n):
    n['e'] = 234
    assert n == {'a': {'b': {'c': 123}}, 'd': {'e': 234}, 'f': {'e': 234}}


def test_mod_multiple_keys_single_target(n):
    n['d/e'] = 234
    assert n == {'a': {'b': {'c': 123}}, 'd': {'e': 234}, 'f': {'e': 789}}


def test_mod_one_out_of_many_keys():
    k = nd.NestedDict({'a': {'b': {'c': {'e': 123}}}, 'd': {'e': 123}, 'f': {'c': {'e': 123}}})

    k['a/b/c/e'] = 234
    assert k == {'a': {'b': {'c': {'e': 234}}}, 'd': {'e': 123}, 'f': {'c': {'e': 123}}}

    k['b/c/e'] = 345
    assert k == {'a': {'b': {'c': {'e': 345}}}, 'd': {'e': 123}, 'f': {'c': {'e': 123}}}


def test_mod_ambiguous_key():
    k = nd.NestedDict({'a': {'b': {'c': {'e': 123}}}, 'd': {'e': 123}, 'f': {'c': {'e': 123}}})

    with raises(KeyError):
        k['c/e'] = 456
