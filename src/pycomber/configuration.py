#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycomber.value_objects import ImmutableDict
from pycomber.strategies import MergeList, MergeDict, MergeSet, MergePrimitives


class ConfigurationAbstract(object):
    """Abstract class for every configuration instance"""

    def __call__(self, merger):
        """Performs configuration for given merger instance

        Arguments:
            :param    merger: merge manager instance to be configured
            :type     merger: pycomber.manager.Manager
        :returns: None
        :raises: NotImplementedError
        """
        raise NotImplementedError("Implement __call__ method")


class ConfigurationAggregate(ConfigurationAbstract):

    def __init__(self, *args):
        self._inner = args

    def __call__(self, merger):
        """Performs configuration for given merger instance

        Arguments:
            :param    merger: merge manager instance to be configured
            :type     merger: pycomber.manager.Manager
        :returns: None
        """
        [c(merger) for c in self._inner]


class ConfigurationDefault(ConfigurationAbstract):
    """Default configuration for merge Manager"""

    def __call__(self, merger):
        """Performs configuration for given merger instance

        Arguments:
            :param    merger: merge manager instance to be configured
            :type     merger: pycomber.manager.Manager
        :returns: None
        """
        NoneType = type(None)
        # complex types
        merger.set_strategy(MergeList(merger), list)
        merger.set_strategy(MergeDict(merger), dict)
        merger.set_strategy(MergeSet(merger), set)
        # primitives
        merger.set_strategy(MergePrimitives(merger), \
                (str, int, float, complex, bool, NoneType))

        # factory for NoneTypes
        merger.set_factory(NoneType, self._none)

    def _none(self, val):
        """Helper function that returns None

        :returns: None
        """
        return None


class ConfigurationImmutable(ConfigurationAbstract):
    """Configures merger to produce immutable instances of input objects"""

    def __call__(self, merger):
        """Performs configuration for given merger instance

        Arguments:
            :param    merger: merge manager instance to be configured
            :type     merger: pycomber.manager.Manager
        :returns: None
        """
        merger.set_factory(list, tuple)
        merger.set_factory(dict, ImmutableDict)
        merger.set_factory(set, frozenset)
