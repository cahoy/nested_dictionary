from src import NestedDict as nd
from pytest import fixture, raises


@fixture(scope='module')
def x():
    return nd.NestedDict()


@fixture(scope='module')
def c():
    val = nd.NestedDict()
    val[123] = 'abc'
    val[456] = 'def'
    val[789] = 'ghi'
    return val


@fixture(scope='module')
def n():
    return nd.NestedDict()


def test_quick_assign(x):
    x[123] = 'abc'
    x['def'] = 456

    assert x[123] == 'abc'
    assert x['def'] == 456


def test_update(x):
    x.update({'foo': 'bar'})
    x.update(baz='qux')

    assert x['foo'] == 'bar'
    assert x['baz'] == 'qux'


def test_setdefault(x):
    x.setdefault(key='y', default='z')
    x.setdefault(key='y', default='w')

    assert x['y'] == 'z'


def test_length(c):
    assert len(c) == 3


def test_del(x):
    del x[123]
    with raises(KeyError):
        assert x[123]


def test_iter_key(c):
    s = set()
    for key in c:
        s.add(key)

    assert s == {123, 456, 789}


def test_iter_item(c):
    s = set()
    for key, val in c.items():
        s.add((key, val))

    assert s == {(123, 'abc'), (456, 'def'), (789, 'ghi')}


# TUPLE STYLE
def test_set_first_branch(n):
    n.clear()
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


# BRACKET STYLE
def test_set_deep_keys_with_bracket(n):
    n.clear()
    n['a'] = {}
    n['a']['b'] = {}
    n['b']['c'] = None
    n['c'] = 123
    n['d'] = None

    assert n == {'a': {'b': {'c': 123}}, 'd': None}


def test_set_deep_keys_with_non_bracket(n):
    n.clear()
    n['a'] = None
    with raises(Exception):
        n['a']['b'] = None  # internally, executing __getitem__ then attempt to perform __setitem__


def test_get_with_partial_keys(n):
    n.clear()
    n.update({'a': {'b': {'c': 123}}, 'd': None})

    assert n['a']['b']['c'] == 123
    assert n['b']['c'] == 123
    assert n['c'] == 123


# BACKSLASH STYLE
def test_set_empty_dict_with_two_keys_with_slash(n):
    n.clear()
    n['a/b'] = 123
    assert n == {'a': {'b': 123}}


def test_set_empty_dict_with_three_keys_with_slash(n):
    n.clear()
    n['a/b/c'] = 123
    assert n == {'a': {'b': {'c': 123}}}


def test_set_non_empty_dict_with_slash(n):
    n.clear()
    n['a'] = {}
    n['a']['b'] = {}
    n['b']['c'] = None
    n['c'] = 123
    n['d'] = None

    n['d/e'] = 456
    assert n == {'a': {'b': {'c': 123}}, 'd': {'e': 456}}

    n['a/b/c'] = 789
    assert n == {'a': {'b': {'c': 789}}, 'd': {'e': 456}}


def test_get_with_slash(n):
    n.clear()
    n['a'] = {}
    n['a']['b'] = {}
    n['b']['c'] = None
    n['c'] = 123
    n['d'] = None

    assert n['a/b/c'] == 123
