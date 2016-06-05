#Nested Dict
![build](https://img.shields.io/badge/build-passing-brightgreen.svg "passing") ![license](https://img.shields.io/badge/license-MIT%20License-blue.svg) ![tests](https://img.shields.io/badge/tests-passing-green.svg)

### Installation

    pip install easy_dict


### Usage
    from easy_dict import NestedDict
    d = {'a': {'b': {'c': 123}}, 'd': {'e': 456}}
    n = NestedDict(d)

These following assignments to nested dict object are valid.

    n = NestedDict()
    n['foo'] = 'bar'
    n.update({'foo': 'bar'})
    n.setdefault(key='foo', default='bar')
    
If the key is a string with <code> '/' </code>, trigger the nested function.

    n['a/b/c'] = 123
    assert n == {'a': {'b': {'c': 123}}}

Access nested content easily.

    k = NestedDict({'a': {'b': {'c': 123}}, 'd': {'e': 456}})

    assert k['a']['b']['c'] == 123
    assert k['b']['c'] == 123
    assert k['c'] == 123
    
    assert k[['a', 'b', 'c']] == 123
    assert k[['b', 'c']] == 123
    assert k[['c']] == 123
    
    assert k['a/b/c'] == 123
    assert k['b/c'] == 123

