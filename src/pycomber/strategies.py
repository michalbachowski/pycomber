#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools


class MergeAbstract(object):
    """Abstract class to any Merge instance"""

    def __init__(self, merger):
        """Class initialization

        Arguments:
            :param    manager: merg manager instance
            :param    manager: pycomber.manager.Manager
        """
        self._merger = merger

    def __call__(self, merge_from, merge_to):
        """Merges given objects

        Arguments:
            :param    merge_from: merge from this object
            :type     merge_from: object
            :param    merge_to: merge to this object
            :type     merge_to: object
        :returns: object -- merged instances
        :raises: NotImplementedError
        """
        raise NotImplementedError("Method __call__ is not implemented")


class MergeList(MergeAbstract):
    """Merger for list type. Joins two list and eliminates duplicates
    Recursively applies merge to all values"""

    def __call__(self, merge_from, merge_to):
        """Merges given objects

        Arguments:
            :param    merge_from: merge from this object
            :type     merge_from: object
            :param    merge_to: merge to this object
            :type     merge_to: object
        :returns: object -- merged instances
        """
        return map(self._merger, set(itertools.chain(merge_from, merge_to)))


class MergeListOverride(MergeList):
    """Merger for list type. Overrides merge_to with merge_from
    Recursively applies merge to all values"""

    def __call__(self, merge_from, merge_to):
        """Merges given objects

        Arguments:
            :param    merge_from: merge from this object
            :type     merge_from: object
            :param    merge_to: merge to this object
            :type     merge_to: object
        :returns: object -- merged instances
        """
        return MergeList.__call__(self, merge_from, [])


class MergeSet(MergeAbstract):
    """Merger for set type. Joins two sets together
    Recursively applies merge to all values"""

    def __call__(self, merge_from, merge_to):
        """Merges given objects

        Arguments:
            :param    merge_from: merge from this object
            :type     merge_from: object
            :param    merge_to: merge to this object
            :type     merge_to: object
        :returns: object -- merged instances
        """
        return [self._merger(item) for item in merge_from | merge_to]


class MergeSetOverride(MergeSet):
    """Merger for set type. Overrides merge_to with merge_from.
    Recursively applies merge to all values"""

    def __call__(self, merge_from, merge_to):
        return MergeSet.__call__(self, merge_from, set())


class MergeDict(MergeAbstract):
    """Merger for dict type. Adds missing keys from merge_from to merge_to.
    Recursively merges all keys in common."""

    def __call__(self, merge_from, merge_to):
        """Merges given objects

        Arguments:
            :param    merge_from: merge from this object
            :type     merge_from: object
            :param    merge_to: merge to this object
            :type     merge_to: object
        :returns: object -- merged instances
        """
        out = {}
        for (group_key, group_items) in self._grouped(self._sorted(\
                self._chained(merge_from, merge_to))):
            group_values = self._extract_values_for_groups(group_items)
            out[group_key] = self._merge_values(group_values)
        return out

    def _key_func(self, items):
        """Function that fetches key for given (key, value) pair

        Arguments:
            :param    items: list with (key, value) pair from dict
            :param    items: list
        :returns: object
        :raises: IndexError
        """
        return items[0]

    def _chained(self, merge_from, merge_to):
        """Chains list of (key, value) pairs from given dictionaries

        Arguments:
            :param    merge_from: merge from this object
            :type     merge_from: object
            :param    merge_to: merge to this object
            :type     merge_to: object
        :returns: iterator -- iterator with all values from both dict's
        """
        return itertools.chain(merge_from.iteritems(), merge_to.iteritems())

    def _sorted(self, chained_dicts):
        """Sorts list of (key, value) pairs

        Arguments:
            :param    chained_dicts: iterator of (key, value) pairs
            :type     chained_dicts: iterator
        :returns: iterator
        """
        return sorted(chained_dicts, key=self._key_func)

    def _grouped(self, sorted_dicts):
        """Groups list of (key, value) pairs

        Arguments:
            :param    sorted_dicts: sorted iterator of (key, value) pairs
            :type     sorted_dicts: iterator
        :returns: iterator
        """
        return itertools.groupby(sorted_dicts, key=self._key_func)

    def _extract_values_for_groups(self, group_items):
        """Extracts values from list of grouped data from dict.

        Arguments:
            :param    group_items: list of grouped data from dict:
                                    [(group_key, [(key, value), (key, value)]),]
            :param    group_items: iterator
        :returns: list
        """
        return list(itertools.imap(lambda i: i[1], group_items))

    def _merge_values(self, group_values):
        """Performs actual merge

        Arguments:
            :param    group_values: list of values in common (1 or 2 elements)
            :param    group_values: list
        :returns: object
        """
        return self._merger(*group_values)


class MergeDictOverride(MergeDict):
    """Merger for dict type. Overrides merge_to with merge_from.
    Recursively applies merge to all values"""

    def _merge_values(self, group_values):
        """Performs actual merge

        Arguments:
            :param    group_values: list of values in common (1 or 2 elements)
            :param    group_values: list
        :returns: object
        """
        return self._merger(group_values[0])


class MergePrimitives(MergeAbstract):

    def __call__(self, merge_from, merge_to):
        """Merges given objects

        Arguments:
            :param    merge_from: merge from this object
            :type     merge_from: object
            :param    merge_to: merge to this object
            :type     merge_to: object
        :returns: object -- merged instances
        """
        return merge_from


class MergeNone(MergeAbstract):

    def __call__(self, merge_from, merge_to):
        """Merges given objects

        Arguments:
            :param    merge_from: merge from this object
            :type     merge_from: object
            :param    merge_to: merge to this object
            :type     merge_to: object
        :returns: object -- merged instances
        """
        if merge_from is None:
            return merge_to
        return merge_from
