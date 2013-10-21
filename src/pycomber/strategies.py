#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools


class MergeAbstract(object):

    def __init__(self, merger):
        self._merger = merger

    def __call__(self, merge_from, merge_to):
        raise NotImplementedError("Method __call__ is not implemented")


class MergeList(MergeAbstract):

    def __call__(self, merge_from, merge_to):
        return map(self._merger, set(itertools.chain(merge_from, merge_to)))


class MergeListOverride(MergeList):

    def __call__(self, merge_from, merge_to):
        return MergeList.__call__(self, merge_from, [])


class MergeSet(MergeAbstract):

    def __call__(self, merge_from, merge_to):
        return [self._merger(item) for item in merge_from | merge_to]


class MergeSetOverride(MergeSet):

    def __call__(self, merge_from, merge_to):
        return MergeSet.__call__(self, merge_from, set())


class MergeDict(MergeAbstract):

    def __call__(self, merge_from, merge_to):
        out = {}
        for (group_key, group_items) in self._grouped(self._sorted(\
                self._chained(merge_from, merge_to))):
            group_values = self._extract_values_for_groups(group_items)
            out[group_key] = self._merge_values(group_values)
        return out

    def _key_func(self, items):
        return items[0]

    def _chained(self, merge_from, merge_to):
        return itertools.chain(merge_from.iteritems(), merge_to.iteritems())

    def _sorted(self, chained_dicts):
        return sorted(chained_dicts, key=self._key_func)

    def _grouped(self, sorted_dicts):
        return itertools.groupby(sorted_dicts, key=self._key_func)

    def _extract_values_for_groups(self, group_items):
        return list(itertools.imap(lambda i: i[1], group_items))

    def _merge_values(self, group_values):
        return self._merger(*group_values)


class MergeDictOverride(MergeDict):

    def _merge_values(self, group_values):
        return self._merger(group_values[0])


class MergePrimitives(MergeAbstract):

    def __call__(self, merge_from, merge_to):
        return merge_from


class MergeNone(MergeAbstract):

    def __call__(self, merge_from, merge_to):
        if merge_from is None:
            return merge_to
        return merge_from
