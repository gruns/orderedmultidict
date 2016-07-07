# omdict API

### Nomenclature

Many of omdict's methods contain the word __list__ or __all__. __list__ in a
method name indicates that method interacts with a list of values instead of a
single value. __all__ in a method name indicates that method interacts with the
ordered list of all items, including multiple items with the same key.

Here's an example illustrating __getlist(key, default=[])__, a __list__ method,
and __allitems()__, an __all__ method.

```python
>>> from orderedmultidict import omdict
>>> omd = omdict([(1,1), (2,2), (1,11)])
>>> omd.items()
[(1, 1), (2, 2)]
>>> omd.allitems()
[(1, 1), (2, 2), (1, 11)]
>>> omd.get(1)
1
>>> omd.getlist(1)
[1, 11]
```

So __list__ denotes a list of values, and __all__ denotes all items.

Simple.


### Method parity with dict

All [dict](http://docs.python.org/library/stdtypes.html#dict) methods behave
identically on omdict objects.


### Initialization and Updates

omdict objects can be initialized from a dictionary or a list of key:value
items.

```python
>>> omd = omdict()
>>> omd.allitems()
[]
>>> omd = omdict({1:1, 2:2, 3:3})
>>> omd.allitems()
[(1, 1), (2, 2), (3, 3)]
>>> omd = omdict([(1,1), (2,2), (3,3), (1,1)])
>>> omd.allitems()
[(1, 1), (2, 2), (3, 3), (1, 1)]
```

__load(mapping)__ can be used at any time to reinitialize an omdict.

```python
>>> omd.load({4:4, 5:5})
>>> omd.allitems()
[(4, 4), (5, 5)]
>>> omd = omdict([(1,1), (2,2), (3,3)])
>>> omd.allitems()
[(1, 1), (2, 2), (3, 3)]
>>> omd.load([(6,6), (6,6)])
>>> omd.allitems()
[(6, 6), (6, 6)]
```

__update([mapping])__ updates the dictionary with items from __mapping__, one
item per key like
[dict.update([mapping])](http://docs.python.org/library/stdtypes.html#dict.update).
__updateall([mapping])__ updates the dictionary with all items from
__mapping__. Key order is preserved - existing keys are updated with values from
__mapping__ before any new items are added.

```python
>>> omd = omdict()
>>> omd.update([(1,1), (2,2), (1,11), (2,22)])
>>> omd.items()
[(1, 11), (2, 22)]
>>> omd.allitems()
[(1, 11), (2, 22)]
>>> omd.updateall([(2,'replaced'), (1,'replaced'), (2,'added'), (1,'added')])
>>> omd.allitems()
[(1, 'replaced'), (2, 'replaced'), (2, 'added'), (1, 'added')]
```


### Getters, Setters, and Adders

__omd[key]__ behaves identically to
[dict\[key\]](http://docs.python.org/library/stdtypes.html#dict). If __key__ has
multiple values, only its first value is returned.

```python
>>> omd = omdict([(1,1), (1,'not me')])
>>> omd[1]
1
```

__omd[key] = value__ behaves identically to [dict\[key\] =
value](http://docs.python.org/library/stdtypes.html#dict). If __key__ has
multiple values, they will all be deleted and replaced with __value__.

```python
>>> omd = omdict([(1,'deleted'), (1,'deleted')])
>>> omd[1] = 1
>>> omd[1]
1
```

__del omd[key]__ behaves identically to [del
dict\[key\]](http://docs.python.org/library/stdtypes.html#dict). If __key__ has
multiple values, all of them will be deleted.

```python
>>> omd = omdict([(1,1), (1,11)])
>>> del omd[1]
>>> omd.allitems()
[]
```

__get(key, default=None)__ behaves identically to [dict.get(key,
default=None)](http://docs.python.org/library/stdtypes.html#dict.get). If
__key__ has multiple values, only its first value is returned.

```python
>>> omd = omdict([(1,1), (1,2)])
>>> omd.get(1)
1
>>> omd.get(404, 'sup')
'sup'
```

__getlist(key, default=[])__ is like get(key, default=None) except it returns
the list of values assocaited with __key__.

```python
>>> omd = omdict([(1,1), (1,11), (2,2)])
>>> omd.getlist(1)
[1, 11]
>>> omd.getlist(2)
[2]
>>> omd.getlist(404, 'sup')
'sup'
```

__set(key, value=None)__ sets __key__'s value to __value__. Identical in
function to omd[key] = value. Returns the omdict object for method chaining.

```python
>>> omd = omdict([(1,1), (1,11), (1,111)])
>>> omd.set(1, 1)
>>> omd.getlist(1)
[1]
>>> omd.set(1, 11).set(2, 2)
>>> omd.allitems()
[(1, 11), (2, 2)]
```

__setlist(key, values=[])__ sets __key__'s list of values to __values__. Returns
the omdict object for method chaining.

```python
>>> omd = omdict([(1,1), (2,2)])
>>> omd.setlist(1, ['replaced', 'appended'])
>>> omd.allitems()
[(1, 'replaced'), (2, 2), (1, 'appended')]
>>> omd.setlist(1, ['onlyme'])
>>> omd.allitems()
[(1, 'onlyme'), (2, 2)]
```

__setdefault(key, default=None)__ behaves identically to [dict.setdefault(key,
default=None)](http://docs.python.org/library/stdtypes.html#dict.setdefault).

```python
>>> omd = omdict([(1,1)])
>>> omd.setdefault(1)
1
>>> omd.setdefault(2, None)
>>> omd.allitems()
[(1, 1), (2, None)]
```

__setdefaultlist(key, defaultlist=[None])__ is like setdefault(key, default=None)
except a list of values for __key__ is adopted. If __defaultlist__ isn't
provided, __key__'s value becomes None.

```python
>>> omd = omdict([(1,1)])
>>> omd.setdefaultlist(1)
[1]
>>> omd.setdefaultlist(2, [2, 22])
[2, 22]
>>> omd.allitems()
[(1, 1), (2, 2), (2, 22)]
>>> omd.setdefaultlist(3)
[None]
>>> print omd[3]
None
```

__add(key, value=None)__ adds __value__ to the list of values for __key__.
Returns the omdict object for method chaining.

```python
>>> omd = omdict()
>>> omd.add(1, 1)
>>> omd.allitems()
[(1, 1)]
>>> omd.add(1, 11).add(2, 2)
>>> omd.allitems()
[(1, 1), (1, 11), (2, 2)]
```

__addlist(key, valuelist=[])__ adds the values in __valuelist__ to the list of
values for __key__. Returns the omdict object for method chaining.

```python
>>> omd = omdict([(1,1)])
>>> omd.addlist(1, [11, 111])
>>> omd.allitems()
[(1, 1), (1, 11), (1, 111)]
>>> omd.addlist(2, [2]).addlist(3, [3, 33])
>>> omd.allitems()
[(1, 1), (1, 11), (1, 111), (2, 2), (3, 3), (3, 33)]
```


### Groups and Group Iteration

__items([key])__ behaves identically to
[dict.items()](http://docs.python.org/library/stdtypes.html#dict.items) except
an optional __key__ parameter has been added. If __key__ is provided, only items
with key __key__ are returned. __iteritems([key])__ returns an iterator over
items(key). KeyError is raised if __key__ is provided and not in the dictionary.

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.items()
[(1, 1), (2, 2), (3, 3)]
>>> omd.items(1)
[(1, 1), (1, 11), (1, 111)]
```

__keys()__ behaves identically to
[dict.keys()](http://docs.python.org/library/stdtypes.html#dict.keys).
__iterkeys()__ returns an iterator over keys().

__values([key])__ behaves identically to
[dict.values()](http://docs.python.org/library/stdtypes.html#dict.values) except
an optional __key__ parameter has been added. If __key__ is provided, only the
values for __key__ are returned. __itervalues([key])__ returns an iterator over
values(key). KeyError is raised if __key__ is provided and not in the
dictionary.

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.values()
[1, 2, 3]
>>> omd.values(1)
[1, 11, 111]
```

__lists()__ returns a list comprised of the lists of values associated with each
dictionary key. __iterlists()__ returns and iterator over lists().

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.lists()
[[1, 11, 111], [2], [3]]
```

__listitems()__ returns a list of key:valuelist items. __iterlistitems()__
returns an iterator over listitems().

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3), (2,22)])
>>> omd.listitems()
[(1, [1, 11, 111]), (2, [2, 22]), (3, [3])]
```

__allitems([key])__ returns a list of every item in the dictionary, including
multiple items with the same key. If __key__ is provided and in the dictionary,
only items with key __key__ are returned . KeyError is raised if __key__ is
provided and not in the dictionary. __iterallitems([key])__ returns an iterator
over allitems(key).

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.allitems()
[(1, 1), (1, 11), (1, 111), (2, 2), (3, 3)]
```

__allkeys()__ returns a list of the keys of every item in the dictionary.
__iterallkeys()__ returns an iterator over allkeys().

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.allkeys()
[1, 1, 1, 2, 3]
```

__allvalues()__ returns a list of the values of every item in the dictionary.
__iterallvalues()__ returns an iterator over allvalues().

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.allvalues()
[1, 11, 111, 2, 3]
```


### Pops

__pop(key[, default])__ behaves identically to [dict.pop(key\[,
default\])](http://docs.python.org/library/stdtypes.html#dict.pop). If __key__
has multiple values, the first value is returned but all items with key __key__
are popped. KeyError is raised if __default__ isn't provided and __key__ isn't
in the dictionary.

```python
>>> omd = omdict([(1,1), (2,2), (1,11)])
>>> omd.pop(1)
1
>>> omd.allitems()
[(2, 2)]
```

__poplist(key[, default])__ is like pop(key[, default]) except it returns the
list of values for __key__. KeyError is raised if __default__ isn't provided and
__key__ isn't in the dictionary.

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.poplist(1)
[1, 11, 111]
>>> omd.allitems()
[(2, 2), (3, 3)]
>>> omd.poplist(2)
[2]
>>> omd.allitems()
[(3, 3)]
>>> omd.poplist('nonexistent key', 'sup')
'sup'
```

__popvalue(key[, value, default], last=True)__ pops a value for __key__.

If __value__ is not provided, the first or last value for __key__ is popped and
returned.

If __value__ is provided, the first or last (__key__,__value__) item is popped
and __value__ is returned.

If __key__ no longer has any values after a popvalue() call, __key__ is removed
from the dictionary. __default__ is returned if provided and __key__ isn't in
the dictionary. KeyError is raised if __default__ isn't provided and __key__
isn't in the dictionary. ValueError is raised if __value__ is provided but isn't a
value for __key__.

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3), (2,22)])
>>> omd.popvalue(1)
111
>>> omd.allitems()
[(1, 1), (1, 11), (2, 2), (3, 3), (2, 22)]
>>> omd.popvalue(1, last=False)
1
>>> omd.allitems()
[(1, 11), (2, 2), (3, 3), (2, 22)]
>>> omd.popvalue(2, 2)
2
>>> omd.allitems()
[(1, 11), (3, 3), (2, 22)]
>>> omd.popvalue(1, 11)
11
>>> omd.allitems()
[(3, 3), (2, 22)]
>>> omd.popvalue('not a key', default='sup')
'sup'
```

__popitem(fromall=False, last=True)__ pops and returns a key:value item.

If __fromall__ is False, items()[0] is popped if __last__ is False or
items()[-1] is popped if __last__ is True. All remaining items with the same key
are removed.

If __fromall__ is True, allitems()[0] is popped if __last__ is False or
allitems()[-1] is popped if __last__ is True. No other remaining items are
removed, even if they have the same key.

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.popitem()
(3, 3)
>>> omd.popitem(fromall=False, last=False)
(1, 1)
>>> omd.popitem(fromall=False, last=False)
(2, 2)
>>> omd.allitems()
[]

>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.popitem(fromall=True, last=False)
(1, 1)
>>> omd.popitem(fromall=True, last=False)
(1, 11)
>>> omd.popitem(fromall=True, last=True)
(3, 3)
>>> omd.popitem(fromall=True, last=False)
(1, 111)
```

__poplistitem([key], last=True)__ pops and returns a key:valuelist item
comprised of a key and that key's list of values. If __last__ is False, a
key:valuelist item comprised of keys()[0] and its list of values is popped and
returned. If __last__ is True, a key:valuelist item comprised of keys()[-1] and
its list of values is popped and returned. KeyError is raised if the dictionary
is empty or if __key__ is provided and not in the dictionary.

```python
>>> omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
>>> omd.poplistitem(last=True)
(3, [3])
>>> omd.poplistitem(last=False)
(1, [1, 11, 111])
```


### Miscellaneous

__copy()__ returns a shallow copy of the dictionary.

```python
>>> omd = omdict([(1,1), (1,11), (2,2), (3,3)])
>>> copy = omd.copy()
>>> omd == copy
True
>>> isinstance(copy, omdict)
True
```

__clear()__ clears all items.

```python
>>> omd = omdict([(1,1), (1,11), (2,2), (3,3)])
>>> omd.clear()
>>> omd.allitems()
[]
```

__len(omd)__ returns the number of keys in the dictionary, identical to
[len(dict)](http://docs.python.org/library/stdtypes.html#dict).

```python
>>> omd = omdict([(1, 1), (2, 2), (1, 11)])
>>> len(omd)
2
```

__size()__ returns the total number of items in the dictionary.

```python
>>> omd = omdict([(1, 1), (1, 11), (2, 2), (1, 111)])
>>> omd.size()
4
```

__reverse()__ reverses the order of all items in the dictionary and returns the
omdict object for method chaining.

```python
>>> omd = omdict([(1, 1), (2, 2), (3, 3)])
>>> omd.allitems()
[(1, 1), (2, 2), (3, 3)]
>>> omd.reverse()
>>> omd.allitems()
[(3, 3), (2, 2), (1, 1)]
```

__fromkeys(keys[, value])__ behaves identically to [dict.fromkeys(key\[,
value\])](http://docs.python.org/library/stdtypes.html#dict.fromkeys).

__has_key(key)__ behaves identically to
[dict.has_key(key)](http://docs.python.org/library/stdtypes.html#dict.has_key),
but use `key in omd` instead of `omd.has_key(key)` where possible.

