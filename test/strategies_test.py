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
# pycomber modules
#
from pycomber.strategies import MergeAbstract, MergeList, MergeListOverride, \
    MergeSet, MergeSetOverride, MergeTuple, MergeTupleOverride, MergeDict, \
    MergeDictOverride, MergePrimitives, MergeNone


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
        except (TypeError,) as e:
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


class MergeListTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeList
        MergeTestMixin.setUp(self)

    def test_merge_generates_union_of_two_list(self):
        self.assertEqual(list(self.merger([1], [2])), [1, 2])

    def test_merge_returns_unique_values(self):
        self.assertEqual(list(self.merger([1, 2], [2, 3])), [1, 2, 3])
        d = {'a': 1}
        self.assertEqual(list(self.merger([1, d], [d, 2])), [1, 2, d])
        self.assertEqual(list(self.merger([1, 2, d], [d, 2])), [1, 2, d])

    def test_calls_merge_manager_for_each_value(self):
        d = {'a': 1}
        list(self.merger([1, 2, d], [2, 3]))
        self.assertEqual(self.manager.call_count, 4)


class MergeListOverrideTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeListOverride
        MergeTestMixin.setUp(self)

    def test_merge_returns_generator(self):
        self.assertFalse(isinstance(self.merger([1,2], [3]), list))

    def test_merge_overrides_second_list_with_items_from_first_one(self):
        self.assertEqual(list(self.merger([1], [2])), [1])

    def test_merge_returns_unique_values(self):
        self.assertEqual(list(self.merger([1, 2, 2], [2, 3])), [1, 2])
        d = {'a': 1}
        self.assertEqual(list(self.merger([1, d, d], [d, 2])), [1, d])
        self.assertEqual(list(self.merger([1, 2, d, 2, d], [d, 3])), [1, 2, d])

    def test_calls_merge_manager_for_each_value(self):
        d = {'a': 1}
        list(self.merger([1, 2, d], [2, 3]))
        self.assertEqual(self.manager.call_count, 3)


class MergeSetTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeSet
        MergeTestMixin.setUp(self)

    def test_merge_generates_union_of_two_sets(self):
        self.assertEqual(self.merger(set([1, 2]), set([2, 3])), set([1, 2, 3]))
        self.assertEqual(self.merger(set([1, 2]), set([3])), set([1, 2, 3]))

    def test_calls_merge_manager_for_each_key(self):
        self.merger(set([1, 2]), set([2, 3]))
        self.assertEqual(self.manager.call_count, 3)


class MergeSetOverrideTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeSetOverride
        MergeTestMixin.setUp(self)

    def test_merge_overrides_second_set_with_first_one(self):
        self.assertEqual(self.merger(set([1, 2]), set([2, 3])), set([1, 2]))
        self.assertEqual(self.merger(set([1, 2]), set([3])), set([1, 2]))

    def test_calls_merge_manager_for_each_key(self):
        self.merger(set([1, 2]), set([2, 3]))
        self.assertEqual(self.manager.call_count, 2)


class MergeTupleTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeTuple
        MergeTestMixin.setUp(self)

    def test_merge_generates_union_of_two_tuples(self):
        self.assertEqual(self.merger((1, 2), (2, 3)), (1, 2, 3))
        self.assertEqual(self.merger((1, 2), (3,)), (1, 2, 3))

    def test_calls_merge_manager_for_each_key(self):
        self.merger((1, 2), (2, 3))
        self.assertEqual(self.manager.call_count, 3)


class MergeTupleOverrideTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeTupleOverride
        MergeTestMixin.setUp(self)

    def test_merge_overrides_second_tuple_with_first_one(self):
        self.assertEqual(self.merger((1, 2), (2, 3)), (1, 2))
        self.assertEqual(self.merger((1, 2), (3,)), (1, 2))

    def test_calls_merge_manager_for_each_key(self):
        self.merger((1, 2), (2, 3))
        self.assertEqual(self.manager.call_count, 2)


class MergeDictTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeDict
        MergeTestMixin.setUp(self)

    def test_merge_generates_union_of_two_dicts(self):
        self.assertEqual(self.merger({'a': 1}, {'b': 1}), {'a': 1, 'b': 1})
        self.assertEqual(self.merger({'a': 1}, {'a': 2}), {'a': 1})

    def test_merge_of_values_depends_on_merge_manager_configuration(self):
        self.assertEqual(self.merger({'a': 1}, {'a': 2}), {'a': 1})
        self.manager.side_effect = lambda a, b: b
        self.assertEqual(self.merger({'a': 1}, {'a': 2}), {'a': 2})

    def test_calls_merge_manager_for_each_key(self):
        self.merger({'a': 1}, {'a': 2})
        self.assertEqual(self.manager.call_count, 1)
        self.manager.reset_mock()
        self.merger({'a': 1}, {'b': 2})
        self.assertEqual(self.manager.call_count, 2)


class MergeDictOverrideTestCase(unittest.TestCase, MergeTestMixin):

    def setUp(self):
        self.merger_class = MergeDictOverride
        MergeTestMixin.setUp(self)

    def test_merge_overrides_values_from_second_dict_with_first_one(self):
        self.assertEqual(self.merger({'c': 3}, {'d': 4}), {'c': 3})
        self.assertEqual(self.merger({'a': 1}, {'a': 2}), {'a': 1})

    def test_calls_merge_manager_for_each_key(self):
        self.merger({'a': 1}, {'a': 2})
        self.assertEqual(self.manager.call_count, 1)
        self.manager.reset_mock()
        self.merger({'a': 1}, {'b': 2})
        self.assertEqual(self.manager.call_count, 1)


if "__main__" == __name__:
    unittest.main()
