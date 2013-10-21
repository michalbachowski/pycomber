#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
from collections import defaultdict
from pycomber.strategies import MergeAbstract


class Manager(MergeAbstract):

    def __init__(self):
        self._strategies = defaultdict(dict)
        self._factories = {}

    def set_factory(self, base_type, factory):
        if base_type not in self._strategies:
            raise TypeError("%s must be one of default base type: %s" % \
                    (base_type, self._strategies.keys()))
        self._factories[base_type] = factory
        return self

    def get_factory(self, base_type):
        return self._factories[base_type]

    def set_strategy(self, strategy, left_type, right_type=None):
        for (l, r) in self._cartesian_product(left_type, right_type):
            self._strategies[l][r] = strategy
        return self

    def get_strategy(self, left_type, right_type):
        try:
            return self._strategies[left_type][right_type]
        except KeyError:
            raise TypeError("Missing strategy for types %s and %s" % \
                                                        (left_type, right_type))

    def _cartesian_product(self, left_type, right_type):
        lt = self._variable_as_set(left_type)
        if right_type is None:
            rt = lt
        else:
            rt = self._variable_as_set(right_type)
        return itertools.product(lt, rt)

    def _variable_as_set(self, var):
        try:
            len(var)
        except TypeError:
            return set([var])
        else:
            return var

    def __call__(self, merge_from=None, merge_to=None):
        (left_type, right_type) = (type(merge_from), type(merge_to))
        strategy = self.get_strategy(left_type, right_type)
        return self._cast(strategy(merge_from, merge_to))

    def _cast(self, var):
        try:
            return self.get_factory(type(var))(var)
        except KeyError:
            return var
