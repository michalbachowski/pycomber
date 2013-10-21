#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

##
# content bits modules
#
from pycomber.merger import Merger


class MergerPointTestCase(unittest.TestCase):

    def setUp(self):
        self.merger = Merger()

    def test_init_requires_no_arguments(self):
        err = False
        try:
            Merger()
        except AttributeError:
            err = True
        self.assertFalse(err)


if "__main__" == __name__:
    unittest.main()


def a():
    import merger

    a = {'a': 1, 'b': 2, 'c': [3, 33]}
    b = {'b': 22, 'c': [33, 34], 'd': None}
    print merger.MergerImmutable().merge(a, b)
