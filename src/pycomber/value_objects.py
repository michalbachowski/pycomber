#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import MutableMapping


class ImmutableDict(MutableMapping):
    """Configuration value object for immutable dict

    Configuration represented by this class is **Immutable**
    """

    def __init__(self, inner):
        self._inner = inner

    def __getitem__(self, key):
        return self._inner[key]

    def __setitem__(self, key, value):
        raise TypeError("Object is immutable")

    def __delitem__(self, key):
        raise TypeError("Object is immutable")

    def __iter__(self):
        return self._inner.__iter__()

    def __len__(self):
        return self._inner.__len__()

    def __contains__(self, x):
        return self._inner.__contains__(x)
