from pytest import fixture, raises

import easy_dict as nd


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
    # with raises(NotImplementedError):
    x.setdefault(key='y', default='z')
    x.setdefault(key='y', default='w')

    assert x['y'] == 'z'


def test_length(c):
    assert len(c) == 3


def test_del(x):
    del x[123]

    # assert x == {'foo': 'bar', 'baz': 'qux', 'def': 456}
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


def test_set_deep_keys_with_non_bracket(x):
    x.clear()
    x['a'] = None
    with raises(Exception):
        x['a']['b'] = None  # internally, executing __getitem__ then attempt to perform __setitem__