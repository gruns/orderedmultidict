#
# omdict: Ordered Multivalue Dictionary.
#
# Arthur Grunseid
# grunseid.com
# grunseid@gmail.com
#
# License: Build Amazing Things (Unlicense)

try:
  from collections import OrderedDict as odict
except ImportError:
  from ordereddict import OrderedDict as odict
from itertools import imap, izip, izip_longest, repeat

from itemlist import itemlist

_absent = object() # Marker that means no parameter was provided.

class omdict(object):
  """
  omdict: Ordered Multivalue Dictionary.

  A multivalue dictionary is a dictionary that can store multiple values for the
  same key. An ordered multivalue dictionary is a multivalue dictionary that
  retains the order of insertions and deletions.

  Internally, items are stored in a doubly linked list, self._items. A
  dictionary, self._map, is also maintained and stores an ordered list of linked
  list node references, one for each value associated with that key.

  Standard dict methods interact with the first value associated with a given
  key. This means that omdict retains method parity with dict, and a dict object
  can be replaced with an omdict object and all interaction will behave
  identically. All dict methods that retain parity with omdict are:
  
    get(), setdefault(), pop(), popitem(),
    clear(), copy(), update(), fromkeys(), len()
    __getitem__(), __setitem__(), __delitem__(), __contains__(),
    items(), keys(), values(), iteritems(), iterkeys(), itervalues(),

  Optional parameters have been added to some dict methods, but because the
  added parameters are optional, existing use remains unaffected. An optional
  <key> parameter has been added to these methods:

    items(), values(), iteritems(), itervalues()

  New methods have also been added to omdict. Methods with 'list' in their name
  interact with lists of values, and methods with 'all' in their name interact
  with all items in the dictionary, including multiple items with the same key.
 
  The new omdict methods are:
  
    load(), size(), reverse(),
    getlist(), add(), addlist(), set(), setlist(), setdefaultlist(),
    poplist(), popvalue(), popitem(), poplistitem(),
    allitems(), allkeys(), allvalues(), lists(), listitems(),
    iterallitems(), iterallkeys(), iterallvalues(), iterlists(), iterlistitems()

  Explanations and examples of the new methods above can be found in the
  function comments below and online at

    https://github.com/gruns/orderedmultidict

  Additional omdict information and documentation can also be found at the above
  url.
  """
  def __init__(self, mapping=[]):
    # Doubly linked list of itemnodes, each itemnode storing a key:value
    # item.
    self._items = itemlist()

    # Ordered dictionary of keys and itemnode references. Each itemnode
    # reference points to one of that keys values.
    self._map = odict()

    self.load(mapping)

  def load(self, mapping=[]):
    """
    Clear all existing key:value items and import all key:value items from
    <mapping>. If multiple values exist for the same key in <mapping>, they are
    all be imported.

    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.load([(4,4), (4,44), (5,5)])
      omd.allitems() == [(4,4), (4,44), (5,5)]

    Returns: self.
    """
    self.clear()
    self.updateall(mapping)
    return self
    
  def copy(self):
    return self.__class__(self._items)

  def clear(self):
    self._map.clear()
    self._items.clear()

  def size(self):
    """
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.size() == 5

    Returns: Total number of items, including multiple items with the same key.
    """
    return len(self._items)

  @classmethod
  def fromkeys(cls, iterable, value=None):
    return cls([(key, value) for key in iterable])

  def has_key(self, key):
    return key in self

  def update(self, *args, **kwargs):
    self._update_updateall(True, *args, **kwargs)

  def updateall(self, *args, **kwargs):
    """
    Update this dictionary with the items from <mapping>, replacing existing
    key:value items with shared keys before adding new key:value items.

    Example:
      omd = omdict([(1,1), (2,2)])
      omd.updateall([(2,'two'), (1,'one'), (2,222), (1,111)])
      omd.allitems() == [(1, 'one'), (2, 'two'), (2, 222), (1, 111)]

    Returns: self.
    """
    self._update_updateall(False, *args, **kwargs)
    return self

  def _update_updateall(self, replace_at_most_one, *args, **kwargs):
    leftovers = []
    newvalues = dict()
    def process_items(iterator):
      for key, value in iterator:
        # If there are existing items with key <key> that have yet to be marked
        # for replacement, mark that item's value to be replaced by <value> by
        # appending it to <newvalues>.
        if key in self and key not in newvalues:
          newvalues[key] = [value]
        elif (key in self and not replace_at_most_one and
              len(newvalues[key]) < len(self.values(key))):
          newvalues[key].append(value)
        else:
          if replace_at_most_one:
            newvalues[key] = [value]
          else:
            leftovers.append((key, value))

    # Process <args>.
    for mapping in args:
      iterator = mapping
      if hasattr(mapping, 'iterallitems') and callable(mapping.iterallitems):
        iterator = mapping.iterallitems()
      elif hasattr(mapping, 'iteritems') and callable(mapping.iteritems):
        iterator = mapping.iteritems()
      process_items(iterator)
    # Process <kwargs>.
    process_items(kwargs.iteritems())

    # First, replace existing values for each key.
    for key, values in newvalues.iteritems():
      self.setlist(key, values)
    # Then, add the leftover items to the end of the list of all items.
    for key, value in leftovers:
      self.add(key, value)

  def get(self, key, default=None):
    if key in self:
      return self._map[key][0].value
    return default

  def getlist(self, key, default=[]):
    """
    Returns: The list of values for <key> if <key> is in the dictionary, else
    <default>. If <default> is not provided, an empty list is returned.
    """
    if key in self:
      return [node.value for node in self._map[key]]
    return default

  def setdefault(self, key, default=None):
    if key in self:
      return self[key]
    self.add(key, default)
    return default

  def setdefaultlist(self, key, defaultlist=[]):
    """
    Similar to setdefault() except <defaultlist> is a list of values to set for
    <key>. If <key> already exists, its existing list of values is returned.

    Returns: List of <key>'s values if <key> exists in the dictionary, otherwise
    <default>.
    """
    if key in self:
      return self.getlist(key)
    self.addlist(key, defaultlist)
    return defaultlist

  def add(self, key, value=None):
    """
    Add <value> to the list of values for <key>. If <key> is not in the
    dictionary, then <value> is added as the sole value for <key>.
    
    Example:
      omd = omdict()
      omd.add(1, 1)  # omd.allitems() == [(1,1)]
      omd.add(1, 11) # omd.allitems() == [(1,1), (1,11)]
      omd.add(2, 2)  # omd.allitems() == [(1,1), (1,11), (2,2)]

    Returns: self.
    """    
    self._map.setdefault(key, [])
    node = self._items.append(key, value)
    self._map[key].append(node)
    return self

  def addlist(self, key, valuelist=[]):
    """
    Add the values in <valuelist> to the list of values for <key>. If <key> is
    not in the dictionary, the values in <valuelist> become the values for
    <key>.

    Example:
      omd = omdict([(1,1)])
      omd.addlist(1, [11, 111])
      omd.allitems() == [(1, 1), (1, 11), (1, 111)]
      omd.addlist(2, [2])
      omd.allitems() == [(1, 1), (1, 11), (1, 111), (2, 2)]

    Returns: self.
    """    
    for value in valuelist:
      self.add(key, value)
    return self

  def set(self, key, value=None):
    """
    Sets <key>'s value to <value>. Identical in function to __setitem__().

    Returns: self.
    """
    self[key] = value
    return self

  def setlist(self, key, values=[]):
    """
    Sets <key>'s list of values to <values>. Existing items with key <key> are
    first replaced with new values from <values>. Any remaining old items that
    haven't been replaced with new values are deleted, and any new values from
    <values> that don't have corresponding items with <key> to replace are
    appended to the end of the list of all items.

    Example:
      omd = omdict([(1,1), (2,2)])
      omd.setlist(1, [11, 111])
      omd.allitems() == [(1,11), (2,2), (1,111)]

      omd = omdict([(1,1), (1,11), (1,111)])
      omd.setlist(1, [None])
      omd.allitems() == [(1,None), (2,2)]

    Returns: self.
    """
    it = izip_longest(list(self._map.get(key, [])), values, fillvalue=_absent)
    for node, value in it:
      if node is not _absent and value is not _absent:
        node.value = value
      elif node is _absent:
        self.add(key, value)
      elif value is _absent:
        self._map[key].remove(node)
        self._items.removenode(node)
    return self

  def pop(self, key, default=_absent):
    if key in self:
      return self.poplist(key)[0]
    elif key not in self._map and default is not _absent:
      return default
    raise KeyError(key)

  def poplist(self, key, default=_absent):
    """
    If <key> is in the dictionary, pop it and return its list of values. If
    <key> is not in the dictionary, return <default>. KeyError is raised if
    <default> is not provided and <key> is not in the dictionary.

    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.poplist(1) == [1, 11, 111]
      omd.allitems() == [(2,2), (3,3)]
      omd.poplist(2) == [2]
      omd.allitems() == [(3,3)]

    Raises: KeyError if <key> isn't in the dictionary and <default> isn't
      provided.
    Returns: List of <key>'s values.
    """
    if key in self:
      values = self.getlist(key)
      del self._map[key]
      for node, nodekey, nodevalue in self._items:
        if nodekey == key:
          self._items.removenode(node)
      return values
    elif key not in self._map and default is not _absent:
      return default
    raise KeyError(key)

  def popvalue(self, key, default=_absent, last=True):
    """
    Pops the first or last value for <key> if <key> is in the dictionary. If
    <key> no longer has any values after a popvalue() call, <key> is removed
    from the dictionary. If <key> isn't in the dictionary and <default> was
    provided, return default. KeyError is raised if <default> is not provided
    and <key> is not in the dictionary.

    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.popvalue(1, last=True) == 111
      omd.allitems == [(1,1), (1,11), (2,2), (3,3)]
      omd.popvalue(1) == 1
      omd.allitems() == [(1,11), (2,2), (3,3)]

    Params:
      last: Boolean whether to return <key>'s first value (<last> is False) or
        last value (<last> is True).
    Raises: KeyError if <key> isn't in the dictionary and <default> isn't
      provided.
    Returns: The first or last of <key>'s values.
    """
    if key in self:
      node = self._map[key].pop(-1 if last else 0)
      if not self._map[key]:
        del self._map[key]
      self._items.removenode(node)
      return node.value
    elif key not in self._map and default is not _absent:
      return default
    raise KeyError(key)

  def popitem(self, fromall=False, last=True):
    """
    Pop and return a key:value item. If <fromall> is False, items()[0] is popped
    if <last> is False or items()[-1] is popped if <last> is True. If <fromall>
    is True, allitems()[0] is popped if <last> is False or allitems()[-1] is
    popped if <last> is True.

    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.popitem() == (3,3)
      omd.popitem(fromall=False, last=False) == (1,1)
      omd.popitem(fromall=False, last=False) == (2,2)

      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.popitem(fromall=True, last=False) == (1,1)
      omd.popitem(fromall=True, last=False) == (1,11)
      omd.popitem(fromall=True, last=True) == (3,3)
      omd.popitem(fromall=True, last=False) == (1,111)

    Params:
      fromall: Whether to pop an item from items() (<fromall> is True) or
        allitems() (<fromall> is False).
      last: Boolean whether to pop the first item or last item of items() or
        allitems().
    Raises: KeyError if the dictionary is empty.
    Returns: The first or last item from item() or allitem().
    """
    if not self._items:
      raise KeyError('popitem(): %s is empty' % self.__class__.__name__)

    if fromall:
      node = self._items[-1 if last else 0]
      key, value = node.key, node.value
      return key, self.popvalue(key, last=last)
    else:
      key = self._map.keys()[-1 if last else 0]
      return key, self.pop(key)

  def poplistitem(self, last=True):
    """
    Pop and return a key:valuelist item comprised of a key and that key's list
    of values. If <last> is False, a key:valuelist item comprised of keys()[0]
    and its associated list of values are popped and returned. If <last> is
    True, a key:valuelist item comprised of keys()[-1] and its associated list
    of values are popped and returned.

    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.poplistitem(last=True) == (3,[3])
      omd.poplistitem(last=False) == (1,[1,11,111])

    Params:
      last: Boolean whether to pop the first or last key and its associated list
        of values.
    Raises: KeyError if the dictionary is empty.
    Returns: A two-tuple comprised of the first or last key and its associated
      list of values.
    """
    if not self._items:
      raise KeyError('poplistitem(): %s is empty' % self.__class__.__name__)

    key = self.keys()[-1 if last else 0]
    return key, self.poplist(key)

  def items(self, key=_absent):
    """
    Raises: KeyError if <key> is provided and not in the dictionary.
    Returns: List created from iteritems(<key>). Only items with key <key> are
      returned if <key> is provided and is a dictionary key.
    """
    return list(self.iteritems(key))

  def keys(self):
    return list(self.iterkeys())

  def values(self, key=_absent):
    """
    Raises: KeyError if <key> is provided and not in the dictionary.
    Returns: List created from itervalues(<key>).If <key> is provided and is a
      dictionary key, only values of items with key <key> are returned.
    """
    if key is not _absent and key in self._map:
      return list(self.getlist(key))
    return list(self.itervalues())

  def lists(self):
    """
    Returns: List created from iterlists().
    """
    return list(self.iterlists())

  def listitems(self):
    """
    Returns: List created from iterlistitems().
    """
    return list(self.iterlistitems())

  def iteritems(self, key=_absent):
    """
    Parity with dict.iteritems() except the optional <key> parameter has been
    added. If <key> is provided, only items with the provided key are iterated
    over. KeyError is raised if <key> is provided and not in the dictionary.
    
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.iteritems(1) -> (1,1) -> (1,11) -> (1,111)
      omd.iteritems() -> (1,1) -> (1,11) -> (1,111) -> (2,2) -> (3,3)

    Raises: KeyError if <key> is provided and not in the dictionary.
    Returns: An iterator over the items() of the dictionary, or only items with
      the key <key> if <key> is provided.
    """
    if key is not _absent:
      if key in self:
        return iter([(node.key,node.value) for node in self._map[key]])
      raise KeyError(key)
    return iter([(key,nodes[0].value) for (key,nodes) in self._map.iteritems()])

  def iterkeys(self):
    return self._map.iterkeys()

  def itervalues(self, key=_absent):
    """
    Parity with dict.itervalues() except the optional <key> parameter has been
    added. If <key> is provided, only values from items with the provided key
    are iterated over. KeyError is raised if <key> is provided and not in the
    dictionary.
    
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.itervalues(1) -> 1 -> 11 -> 111
      omd.itervalues() -> 1 -> 11 -> 111 -> 2 -> 3

    Raises: KeyError if <key> is provided and isn't in the dictionary.
    Returns: An iterator over the values() of the dictionary, or only the values
      of key <key> if <key> is provided.
    """
    if key is not _absent:
      if key in self:
        return iter([node.value for node in self._map[key]])
      raise KeyError(key)
    return iter([nodes[0].value for nodes in self._map.itervalues()])

  def allitems(self, key=_absent):
    '''
    Raises: KeyError if <key> is provided and not in the dictionary.
    Returns: List created from iterallitems(<key>).
    '''    
    return list(self.iterallitems(key))

  def allkeys(self):
    '''
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.allkeys() == [1,1,1,2,3]

    Returns: List created from iterallkeys().
    '''    
    return list(self.iterallkeys())

  def allvalues(self, key=_absent):
    '''
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.allvalues() == [1,11,111,2,3]
      omd.allvalues(1) == [1,11,111]

    Raises: KeyError if <key> is provided and not in the dictionary.
    Returns: List created from iterallvalues(<key>).
    '''    
    return list(self.iterallvalues(key))

  def iterallitems(self, key=_absent):
    '''
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.iterallitems() == (1,1) -> (1,11) -> (1,111) -> (2,2) -> (3,3)
      omd.iterallitems(1) == (1,1) -> (1,11) -> (1,111)

    Raises: KeyError if <key> is provided and not in the dictionary.
    Returns: An iterator over every item in the diciontary. If <key> is
      provided, only items with the key <key> are iterated over.
    '''
    if key is not _absent:
      return self.iteritems(key) # Raises KeyError if <key> is not in self._map.
    return self._items.iteritems()

  def iterallkeys(self):
    '''
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.iterallkeys() == 1 -> 1 -> 1 -> 2 -> 3
        
    Returns: An iterator over the keys of every item in the dictionary.
    '''
    return self._items.iterkeys()

  def iterallvalues(self, key=_absent):
    '''
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.iterallvalues() == 1 -> 11 -> 111 -> 2 -> 3
        
    Returns: An iterator over the values of every item in the dictionary.
    '''
    if key is not _absent:
      if key in self:
        return iter(self.getlist(key))
      raise KeyError(key)
    return self._items.itervalues()

  def iterlists(self):
    '''
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.iterlists() -> [1,11,111] -> [2] -> [3]
    
    Returns: An iterator over the list comprised of the lists of values for each
    key.
    '''
    return imap(lambda key: self.getlist(key), self)

  def iterlistitems(self):
    """
    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.iterlistitems() -> (1,[1,11,111]) -> (2,[2]) -> (3,[3])

    Returns: An iterator over the list of key:valuelist items.
    """
    return imap(lambda key: (key, self.getlist(key)), self)

  def reverse(self):
    """
    Reverse the order of all items in the dictionary.

    Example:
      omd = omdict([(1,1), (1,11), (1,111), (2,2), (3,3)])
      omd.reverse()
      omd.allitems() == [(3,3), (2,2), (1,111), (1,11), (1,1)]

    Returns: self.
    """
    for key in self._map.iterkeys():
      self._map[key].reverse()
    self._items.reverse()
    return self

  def __eq__(self, other):
    myitems, otheritems = self.iterallitems(), other.iterallitems()
    for item1, item2 in izip_longest(myitems, otheritems, fillvalue=_absent):
      if item1 != item2 or item1 is _absent or item2 is _absent:
        return False
    return True

  def __ne__(self, other):
    return not self.__eq__(other)

  def __len__(self):
    return len(self._map)

  def __iter__(self):
    for key in self.iterkeys():
      yield key

  def __contains__(self, item):
    if hasattr(item, '__len__') and callable(item.__len__) and len(item) == 2:
      return item in self._items
    return item in self._map

  def __getitem__(self, key):
    if key in self:
      return self.get(key)
    raise KeyError(key)

  def __setitem__(self, key, value):
    self.setlist(key, [value])

  def __delitem__(self, key):
    return self.pop(key)

  def __nonzero__(self):
    return bool(self._map)

  def __str__(self):
    return '{%s}' % ', '.join(map(lambda p: '%s: %s'%(p[0], p[1]),
                                  self.iterallitems()))
