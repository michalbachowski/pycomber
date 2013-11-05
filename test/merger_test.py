#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
from functools import partial

##
# pycomber modules
#
from pycomber import merger


class MergerTestCase(unittest.TestCase):

    def test_merger_requires_no_arguments(self):
        err = False
        merger()
        try:
            merger()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_merge(self):
        a = {'a': 1, 'b': 2, 'c': [3, 33], 'e': set([4]), 'f': (5,55)}
        b = {'b': 22, 'c': [33, 34], 'd': None, 'e': set([44]), 'f': (55,56)}
        m1 = merger(a, b)
        self.assertEqual(m1['a'], 1)
        self.assertEqual(m1['b'], 2)
        self.assertEqual(list(m1['c']), [3, 33, 34])
        self.assertEqual(m1['d'], None)
        self.assertEqual(m1['e'], set([4, 44]))
        self.assertEqual(sorted(m1['f']), sorted((5, 55, 56)))

        m2 = merger(b, a)
        self.assertEqual(m2['a'], 1)
        self.assertEqual(m2['b'], 22)
        self.assertEqual(list(m2['c']), [3, 33, 34])
        self.assertEqual(m2['d'], None)
        self.assertEqual(m2['e'], set([4, 44]))
        self.assertEqual(sorted(m2['f']), sorted((5, 55, 56)))


if "__main__" == __name__:
    unittest.main()
