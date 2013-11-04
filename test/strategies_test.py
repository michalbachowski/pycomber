#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
from functools import partial


##
# test helper
#
from testutils import mock


##
# content bits modules
#
from pycomber.strategies import MergeAbstract, MergeList, MergeListOverride, \
    MergeSet, MergeSetOverride, MergeDict, MergeDictOverride, MergePrimitives, \
    MergeNone


class MergeTestMixin(object):

    def setUp(self):
        self.manager = mock.Mock(side_effect = lambda a, b=None: a)
        self.merger = self.merger_class(self.manager)

    def test_init_requires_one_argument(self):
        self.assertRaises(TypeError, self.merger_class)
        err = False
        try:
            self.merger_class(None)
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_instance_is_callable(self):
        self.assertTrue(hasattr(self.merger, '__call__'))

    def test_call_expects_2_arguments(self):
        self.assertRaises(TypeError, self.merger)
        self.assertRaises(TypeError, partial(self.merger, None))
        err=False
        try:
            self.merger(None, None)
        except TypeError, e:
            err='takes exactly ' in e.args[0]
        except:
            pass
        self.assertFalse(err)
        self.assertRaises(TypeError, partial(self.merger, None, None, None))


class MergeAbstractTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeAbstract
        MergeTestMixin.setUp(self)

    def test_call_must_be_implemented(self):
        self.assertRaises(RuntimeError, partial(self.merger, None, None))


class MergeNoneTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeNone
        MergeTestMixin.setUp(self)

    def test_non_None_arguments_is_returned(self):
        self.assertEqual(self.merger(None, 'b'), 'b')
        self.assertEqual(self.merger('a', None), 'a')
        self.assertEqual(self.merger('a', 'b'), 'a')
        self.assertEqual(self.merger(None, None), None)


class MergePrimitivesTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergePrimitives
        MergeTestMixin.setUp(self)

    def test_merge_from_is_alwasy_returned(self):
        self.assertEqual(self.merger(None, 'b'), None)
        self.assertEqual(self.merger('a', None), 'a')
        self.assertEqual(self.merger('a', 'b'), 'a')
        self.assertEqual(self.merger(None, None), None)




if "__main__" == __name__:
    unittest.main()


def a():
    import merger

    a = {'a': 1, 'b': 2, 'c': [3, 33]}
    b = {'b': 22, 'c': [33, 34], 'd': None}
    print merger.MergerImmutable().merge(a, b)
