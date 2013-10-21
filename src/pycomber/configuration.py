#!/usr/bin/env python
# -*- coding: utf-8 -*-
from types import NoneType
from pycomber.value_objects import ImmutableDict
from pycomber.strategies import MergeList, MergeDict, MergeSet, \
        MergePrimitives, MergeNone


class ConfigurationAbstract(object):

    def __call__(self, merger):
        raise NotImplementedError("Implement __call__ method")


class ConfigurationAggregate(ConfigurationAbstract):

    def __init__(self, *args):
        self._inner = args

    def __call__(self, merger):
        [c(merger) for c in self._inner]


class ConfigurationDefault(ConfigurationAbstract):

    def __call__(self, merger):
        # complex types
        merger.set_strategy(MergeList(merger), list)
        merger.set_strategy(MergeDict(merger), dict)
        merger.set_strategy(MergeSet(merger), set)
        # primitives
        merger.set_strategy(MergePrimitives(merger), \
                (str, int, float, long, complex, bool))
        # None
        merger.set_strategy(MergeNone(merger), NoneType, \
            (NoneType, str, int, float, long, complex, bool, list, dict, set))
        merger.set_strategy(MergeNone(merger), \
            (str, int, float, long, complex, bool, list, dict, set), NoneType)
        # factory for NoneTypes
        merger.set_factory(NoneType, self._none)

    def _none(self, val):
        """Helper function that returns

        :returns: None
        """
        return None


class ConfigurationImmutable(ConfigurationAbstract):

    def __call__(self, merger):
        merger.set_factory(list, tuple)
        merger.set_factory(dict, ImmutableDict)
        merger.set_factory(set, frozenset)
