Nested Dict
===========

#### drop-in replacement for the built-in dictionary
These assignments to nested dict object are valid.

    nd = NestedDict()
    nd['foo'] = 'bar'
    nd.update({'foo': 'bar'})
    nd.setdefault(key='foo', default='bar')

#### if the key is a tuple, it trigger special function.

    n['a'] = None
    n[('a', 'b')] = None    # 'b' is a new key at 'a'
    n[('b', 'c')] = 123     # 'c' is a new key at 'b'

    assert n == {'a': {'b': {'c': 123}}}
    
#### if the key is a string with <code> '/' </code>, trigger the nested function

    n['a/b/c'] = 123
    assert n == {'a': {'b': {'c': 123}}}

### access nested content easily

    k = nd.NestedDict({'a': {'b': {'c': 123}}, 'd': {'e': 456}})

    assert k['a']['b']['c'] == 123
    assert k['b']['c'] == 123
    assert k['c'] == 123
    
    assert k[['a', 'b', 'c']] == 123
    assert k[['b', 'c']] == 123
    assert k[['c']] == 123
    
    assert k['a/b/c'] == 123
    assert k['b/c'] == 123

