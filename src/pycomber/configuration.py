#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycomber.value_objects import ImmutableDict
from pycomber.strategies import MergeList, MergeDict, MergeSet, MergeTuple, \
        MergePrimitives


class ConfigurationAbstract(object):
    """Abstract class for every configuration instance"""

    def __call__(self, manager):
        """Performs configuration for given manager instance

        Arguments:
            :param    manager: merge manager instance to be configured
            :type     manager: pycomber.manager.Manager
        :returns: None
        :raises: NotImplementedError
        """
        raise NotImplementedError("Implement __call__ method")


class ConfigurationAggregate(ConfigurationAbstract):
    """Configuration object that aggregates other configurations"""

    def __init__(self, *args):
        """Object constructor

        Arguments:
            :param  *args: inner configuration instances to be aggregated
            :type   *args: set
        """
        self._inner = args

    def __call__(self, manager):
        """Performs configuration for given manager instance

        Arguments:
            :param    manager: merge manager instance to be configured
            :type     manager: pycomber.manager.Manager
        :returns: None
        """
        [c(manager) for c in self._inner]


class ConfigurationComplex(ConfigurationAbstract):
    """Configures manager to merge complex types (dict, list, set)"""

    def __call__(self, manager):
        """Performs configuration for given manager instance

        Arguments:
            :param    manager: merge manager instance to be configured
            :type     manager: pycomber.manager.Manager
        :returns: None
        """
        manager.set_strategy(MergeList(manager), list)
        manager.set_strategy(MergeDict(manager), dict)
        manager.set_strategy(MergeSet(manager), set)
        manager.set_strategy(MergeTuple(manager), tuple)


class ConfigurationPrimitives(ConfigurationAbstract):
    """Configures manager to merge primitives (str, int, float, complex, bool)"""

    def __call__(self, manager):
        """Performs configuration for given manager instance

        Arguments:
            :param    manager: merge manager instance to be configured
            :type     manager: pycomber.manager.Manager
        :returns: None
        """
        manager.set_strategy(MergePrimitives(manager), \
                (str, int, float, complex, bool, type(None)))


class ConfigurationNoneType(ConfigurationAbstract):
    """Configures manager to merge to/from NoneType"""

    def __call__(self, manager):
        """Performs configuration for given manager instance

        Arguments:
            :param    manager: merge manager instance to be configured
            :type     manager: pycomber.manager.Manager
        :returns: None
        """
        NoneType = type(None)
        manager.set_strategy(MergePrimitives(manager), NoneType,
                (str, int, float, complex, bool))
        manager.set_strategy(MergePrimitives(manager),
                (str, int, float, complex, bool), NoneType)

        # factory for NoneTypes
        manager.set_factory(NoneType, self._none)

    def _none(self, val):
        """Helper function that returns None

        :returns: None
        """
        return None


class ConfigurationImmutable(ConfigurationAbstract):
    """Configures manager to produce immutable instances of input objects"""

    def __call__(self, manager):
        """Performs configuration for given manager instance

        Arguments:
            :param    manager: merge manager instance to be configured
            :type     manager: pycomber.manager.Manager
        :returns: None
        """
        manager.set_factory(list, tuple)
        manager.set_factory(dict, ImmutableDict)
        manager.set_factory(set, frozenset)
