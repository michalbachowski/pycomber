#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
from collections import defaultdict
from pycomber.strategies import MergeAbstract


class Manager(MergeAbstract):
    """Merge manager. Needs to be configured before can be used"""

    def __init__(self):
        """Object initialization"""
        self._strategies = defaultdict(dict)
        self._factories = {}

    def set_factory(self, base_type, factory):
        """Sets factory for given base type

        Arguments:
            :param    base_type: base type to cast from
            :type     base_type: type
            :param    factory: factory used to cast variable
            :type     factory: callable
        :returns: Manager -- instance of Manager class (self)
        :raises:  TypeError
        """
        if base_type not in self._strategies:
            raise TypeError("%s must be one of default base type: %s" % \
                    (base_type, self._strategies.keys()))
        self._factories[base_type] = factory
        return self

    def get_factory(self, base_type):
        """Returns factory function for given base type

        Arguments:
            :param    base_type: type to get factory for
            :type     base_type: type
        :returns: callable -- factory method
        :raises:  KeyError
        """
        return self._factories[base_type]

    def set_strategy(self, strategy, left_type, right_type=None):
        """Sets strategy of merging from left_type to right_type

        One can pass either single type or iterator with list of types.
        If "right_type" is ommited - left type would be duplicated.
        Cartesian product of left_type x right_type would be generated
        and all pairs would be used to define strategy for.

        Arguments
            :param    strategy: strategy of merging left_type to right_type
            :type     strategy: callable
            :param    left_type: type to merge from
            :type     left_type: type | iterable
            :param    right_type: type to merge to
            :type     right_type: type | iterable
        :returns: Manager -- instance of Manager class (self)
        """
        for (l, r) in self._cartesian_product(left_type, right_type):
            self._strategies[l][r] = strategy
        return self

    def get_strategy(self, left_type, right_type):
        """Returns merging strategy for left_type (from) and right_type (to)

        Arguments:
            :param    left_type: merge from this type
            :type     left_type: type
            :param    right_type: merge to this type
            :type     right_type: type
        :returns: callable -- factory method
        :raises:  TypeError
        """
        try:
            return self._strategies[left_type][right_type]
        except KeyError:
            raise TypeError("Missing strategy for types %s and %s" % \
                                                        (left_type, right_type))

    def _cartesian_product(self, left_type, right_type):
        """Makes cartesiam product of left_type x right_type

        Arguments:
            :param    left_type: merge from this type
            :type     left_type: type | iterator
            :param    right_type: merge to this type
            :type     right_type: type | iterator
        :returns: generator -- cartesian product of left_type x right_type
        """
        lt = self._variable_as_set(left_type)
        if right_type is None:
            rt = lt
        else:
            rt = self._variable_as_set(right_type)
        return itertools.product(lt, rt)

    def _variable_as_set(self, var):
        """If given variable is iterator - returns this varialbe.
        Otherwise creates iterator containing this one variable

        Arguments:
            :param    var: variable to cast to generator
            :type     var: type | iterator
        :returns: generator
        """
        try:
            len(var)
        except TypeError:
            return set([var])
        else:
            return var

    def __call__(self, merge_from=None, merge_to=None):
        """Merges given instances merge_from and merge_to.
        Creates new instances during merge process.

        Arguments:
            :param    merge_from: merge from this object
            :type     merge_from: object
            :param    merge_to: merge to this object
            :type     merge_to: object
        :returns: object
        :raises: TypeError
        """
        (left_type, right_type) = (type(merge_from), type(merge_to))
        strategy = self.get_strategy(left_type, right_type)
        return self._cast(strategy(merge_from, merge_to))

    def _cast(self, var):
        """Casts given variable using predefined factory (if available)

        Arguments:
            :param    var: variable to cast
            :type     var: type
        :returns: object
        """
        try:
            return self.get_factory(type(var))(var)
        except KeyError:
            return var
