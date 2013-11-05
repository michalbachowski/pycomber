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
from pycomber.manager import Manager


class ManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()

    def test_init_requires_no_arguments(self):
        err = False
        try:
            Manager()
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_set_factory_expects_2_arguments(self):
        self.assertRaises(TypeError, self.manager.set_factory)
        self.assertRaises(TypeError, partial(self.manager.set_factory, None))
        err = False
        try:
            self.manager.set_factory(None, None)
        except TypeError, e:
            err = 'expected at least' in e
        self.assertFalse(err)

    def test_set_factory_requires_existing_strategy_for_given_base_type(self):
        self.assertRaises(TypeError, partial(self.manager.set_factory, int, \
                                                                        None))
        self.manager.set_strategy(None, int, None)
        err = False
        try:
            self.manager.set_factory(int, None)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_get_factory_expects_one_argument(self):
        self.assertRaises(TypeError, self.manager.get_factory)
        self.assertRaises(KeyError, partial(self.manager.get_factory, None))

    def test_get_factory_raises_key_error_for_non_existent_types(self):
        self.assertRaises(KeyError, partial(self.manager.get_factory, None))

    def test_get_factory_returns_previously_set_factory(self):
        self.manager.set_strategy(None, int, None)
        self.manager.set_factory(int, 'a')
        self.assertEqual(self.manager.get_factory(int), 'a')



if "__main__" == __name__:
    unittest.main()
