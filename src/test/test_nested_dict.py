from src.NestedDict import NestedDict
from pytest import fixture, raises


@fixture(scope='module')
def x():
    return NestedDict()


@fixture(scope='module')
def c():
    val = NestedDict()
    val[123] = 'abc'
    val[456] = 'def'
    val[789] = 'ghi'
    return val


@fixture(scope='module')
def n():
    return NestedDict()


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

    # n[('branch', 'key1')] = 'first'
    # assert n == {'branch': {'key1': 'first'}}
    # assert n['branch']['key1'] == 'first'
    #
    # n[('branch', 'key2')] = 'val2'
    # assert n == {'branch': {'key1': 'first', 'key2': 'val2'}}
    # assert n['branch']['key2'] == 'val2'
    #
    # n[('branch', 'key1')] = 'val1'
    # assert n['branch']['key1'] == 'val1'


# def test_set_another_branch(n):
    # n['brunch'] = None
    # n[('brunch', 'key3')] = None
    # assert n['branch'] == {'key1': 'val1', 'key2': 'val2'}
    # assert n['brunch'] == {'key3': None}


# def test_set_nested_branch(n):
    # n[('key3', 'deep_key')] = None
    # assert n['brunch'] == {'key3': {'deep_key': None}}


# def test_set_to_invalid_branch(n):
    # with raises(KeyError):
    #     n[('non_exist_branch', 'key1')] = None


# def test_set_to_non_False_value(n):
    # n['deep_key'] = 'invalid_value'
    # with raises(ValueError):
    #     n[('deep_key', 'new_branch')] = None


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