#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
from functools import partial

##
# content bits modules
#
from pycomber.value_objects import ImmutableDict


class ImmutableDictTestCase(unittest.TestCase):


    def test_init_requires_one_argument(self):
        self.assertRaises(TypeError, ImmutableDict)

    def test_instance_is_immutable(self):
        obj = ImmutableDict({'a': 1})
        self.assertRaises(TypeError, partial(obj.__setitem__, 'a', 2))
        self.assertRaises(TypeError, partial(obj.__setitem__, 'b', 1))
        self.assertRaises(TypeError, partial(obj.__delitem__, 'a'))
        self.assertRaises(TypeError, partial(obj.update, {'b': 1}))

    def test_instance_behaves_as_dict(self):
        obj = ImmutableDict({'a': 1})
        self.assertEqual(obj['a'], 1)
        self.assertEqual(len(obj), 1)
        self.assertTrue('a' in obj)
        self.assertEqual(list(iter(obj)), ['a'])


if "__main__" == __name__:
    unittest.main()
