#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
from functools import partial

##
# test helpers
#
from testutils import mock

##
# pycomber modules
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

    def test_set_factory_allows_to_set_factory(self):
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

    def test_factory_must_be_callable(self):
        self.manager.set_strategy(lambda a, b: a, str, str)
        self.manager.set_factory(str, 'a')
        self.assertRaises(TypeError, partial(self.manager, 'a', 'b'))

    def test_factory_must_accept_2_arguments(self):
        self.manager.set_strategy(lambda a, b: a, str, str)

        self.manager.set_factory(str, lambda: 1)
        self.assertRaises(TypeError, partial(self.manager, 'a', 'b'))

        self.manager.set_factory(str, lambda a: 1)
        err = False
        try:
            self.manager('a', 'b')
        except TypeError:
            err = True
        self.assertFalse(err)

        self.manager.set_factory(str,lambda a, b: 1)
        self.assertRaises(TypeError, partial(self.manager, 'a', 'b'))

    def test_set_strategy_expects_2_arguments(self):
        self.assertRaises(TypeError, self.manager.set_strategy)
        self.assertRaises(TypeError, partial(self.manager.set_strategy, None))
        self.assertRaises(TypeError, partial(self.manager.set_strategy, None, \
                                                            None, None, None))
        err = False
        try:
            self.manager.set_strategy(None, None)
        except TypeError, e:
            err = 'expected at least' in e
        self.assertFalse(err)

    def test_set_strategy_allows_3_arguments(self):
        err = False
        try:
            self.manager.set_strategy(None, None, None)
        except TypeError, e:
            err = 'expected at least' in e
        self.assertFalse(err)

    def test_set_strategy_for_single_types_makes_one_pair(self):
        self.manager.set_strategy('strategy', int, int)
        self.assertEqual(self.manager.get_strategy(int, int), 'strategy')

    def test_set_strategy_for_set_of_types_makes_cartesian(self):
        self.manager.set_strategy('strategy', (int, str), (int, str))
        for a, b in ((int, int), (int, str), (str, str), (str, int)):
            self.assertEqual(self.manager.get_strategy(a, b), 'strategy')

    def test_set_strategy_for_mixed_types_makes_pairs(self):
        self.manager.set_strategy('strategy', int, (int, str))
        for a, b in ((int, int), (int, str)):
            self.assertEqual(self.manager.get_strategy(a, b), 'strategy')
        self.assertRaises(TypeError, partial(self.manager.get_strategy, str, \
                                                                        str))

    def test_set_strategy_treats_string_as_set(self):
        self.manager.set_strategy('strategy', 'ab', 'cd')
        for a, b in (('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd')):
            self.assertEqual(self.manager.get_strategy(a, b), 'strategy')

    def test_get_stragety_returns_predefined_strategy(self):
        self.manager.set_strategy('strategy', 'ab', 'cd')
        for a, b in (('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd')):
            self.assertEqual(self.manager.get_strategy(a, b), 'strategy')

    def test_strategy_must_be_callable(self):
        self.manager.set_strategy('a', str, str)
        self.assertRaises(TypeError, partial(self.manager, 'a', 'b'))

    def test_strategy_must_accept_2_arguments(self):
        self.manager.set_strategy(lambda: 1, str, str)
        self.assertRaises(TypeError, partial(self.manager, 'a', 'b'))

        self.manager.set_strategy(lambda a: 1, str, str)
        self.assertRaises(TypeError, partial(self.manager, 'a', 'b'))

        self.manager.set_strategy(lambda a, b: 1, str, str)
        err = False
        try:
            self.manager('a', 'b')
        except TypeError:
            err = True
        self.assertFalse(err)

        self.manager.set_strategy(lambda a, b, c: 1, str, str)
        self.assertRaises(TypeError, partial(self.manager, 'a', 'b'))

    def test_call_expects_2_arguments(self):
        self.assertRaises(TypeError, self.manager)
        self.assertRaises(TypeError, partial(self.manager, None))
        self.assertRaises(TypeError, partial(self.manager, None, None, None))
        err = False
        try:
            self.manager(None, None)
        except TypeError, e:
            err = 'expected at least' in e
        self.assertFalse(err)

    def test_call_expects_configured_strategy_for_merging(self):
        self.assertRaises(TypeError, partial(self.manager, 'a', 'b'))
        self.manager.set_strategy(lambda a, b: a, str, str)
        err = False
        try:
            self.manager('a', 'b')
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_call_picks_strategies_for_given_type(self):
        s = mock.Mock(return_value='a')
        self.manager.set_strategy(s, str, str)
        self.assertEqual(self.manager('b', 'c'), 'a')
        s.assert_called_once_with('b', 'c')

    def test_call_picks_factory_for_given_value_returned_from_strategy(self):
        s = mock.Mock(return_value=1)
        f = mock.Mock(return_value='g')
        self.manager.set_strategy(s, str, str)
        self.manager.set_factory(int, f)
        self.assertEqual(self.manager('b', 'c'), 'g')
        f.assert_called_once_with(1)


if "__main__" == __name__:
    unittest.main()
