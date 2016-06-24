from pytest import fixture, raises

import easy_dict as nd


@fixture()
def n():
    return nd.NestedDict()


# SETTING WITH TUPLE
# def test_set_first_branch(n):
#     n['a'] = None
#     n[('a', 'b')] = None    # Value at 'a'
#     n[('b', 'c')] = 123
#     n['d'] = None
#
#     assert n == {'a': {'b': {'c': 123}}, 'd': None}
#
#
# def test_set_to_invalid_branch(n):
#     n.clear()
#     n['a'] = None
#     with raises(KeyError):
#         n[('non_exist_branch', 'b')] = None
#
#
# def test_set_to_non_false_value(n):
#     n.clear()
#     n['a'] = 123
#     with raises(ValueError):
#         n[('a', 'b')] = None


def test_add_key_with_anchor(n):
    n.clear()
    n['a'] = None
    n.anchor('a', 'b', None)

    assert n == {'a': {'b': None}}


def test_bad_anchor(n):
    n.clear()
    n['a'] = None
    with raises(KeyError):
        n.anchor('bad_anchor', 'b')


def test_bad_anchored_value(n):
    n.clear()
    n['a'] = 123
    with raises(ValueError):
        n.anchor('a', 'b')
