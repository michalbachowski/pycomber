##
# python standard library
#
import unittest
from functools import partial


##
# test helper
#
from testutils import mock, IsA, IsCallable


##
# content bits modules
#
from pycomber.strategies import MergeAbstract
from pycomber.configuration import ConfigurationAbstract, \
        ConfigurationAggregate, ConfigurationComplex, ConfigurationPrimitives, \
        ConfigurationNoneType, ConfigurationImmutable


class ConfigurationTestMixin(object):

    def setUp(self):
        self.manager = mock.Mock()
        self.conf = self.conf_class()

    def test_init_requires_no_argument(self):
        err = False
        try:
            self.conf_class()
        except AttributeError:
            err = True
        self.assertFalse(err)

    def test_instance_is_callable(self):
        self.assertTrue(hasattr(self.conf, '__call__'))

    def test_call_expects_1_argument(self):
        self.assertRaises(TypeError, self.conf)
        err=False
        try:
            self.conf(None)
        except TypeError, e:
            err='takes exactly ' in e.args[0]
        except:
            pass
        self.assertFalse(err)
        self.assertRaises(TypeError, partial(self.conf, None, None))


class ConfigurationAbstractTestCase(unittest.TestCase, ConfigurationTestMixin):

    def setUp(self):
        self.conf_class = ConfigurationAbstract
        ConfigurationTestMixin.setUp(self)

    def test_call_must_be_implemented(self):
        self.assertRaises(RuntimeError, partial(self.conf, None))


class ConfigurationAggregateTestCase(unittest.TestCase, ConfigurationTestMixin):

    def setUp(self):
        self.conf_class = ConfigurationAggregate
        ConfigurationTestMixin.setUp(self)

    def test_init_accepts_variable_number_of_args(self):
        err = False
        try:
            self.conf_class(None, 1, 'b', 'a')
        except:
            err = True
        self.assertFalse(err)

    def test_call_loops_over_give_args_and_calls_them_with_given_manager(self):
        c1 = mock.Mock()
        c2 = mock.Mock()
        self.conf_class(c1, c2)('a')
        c1.assert_called_with('a')
        c2.assert_called_with('a')


class ConfigurationComplexTestCase(unittest.TestCase, ConfigurationTestMixin):

    def setUp(self):
        self.conf_class = ConfigurationComplex
        ConfigurationTestMixin.setUp(self)

    def test_calls_set_strategy_on_given_object(self):
        self.conf(self.manager)
        self.manager.set_strategy.assert_called_with(IsA(MergeAbstract), \
                IsCallable())


class ConfigurationPrimitivesTestCase(unittest.TestCase, ConfigurationTestMixin):

    def setUp(self):
        self.conf_class = ConfigurationPrimitives
        ConfigurationTestMixin.setUp(self)

    def test_calls_set_strategy_on_given_object(self):
        self.conf(self.manager)
        self.assertTrue(self.manager.set_strategy.call_count > 0)


class ConfigurationNoneTypeTestCase(unittest.TestCase, ConfigurationTestMixin):

    def setUp(self):
        self.conf_class = ConfigurationNoneType
        ConfigurationTestMixin.setUp(self)

    def test_calls_set_strategy_on_given_object(self):
        self.conf(self.manager)
        self.assertTrue(self.manager.set_strategy.call_count > 0)

    def test_calls_set_factory_on_given_object(self):
        self.conf(self.manager)
        self.manager.set_factory.assert_called_with(IsA(type), \
                IsCallable())


class ConfigurationImmutableTestCase(unittest.TestCase, ConfigurationTestMixin):

    def setUp(self):
        self.conf_class = ConfigurationImmutable
        ConfigurationTestMixin.setUp(self)

    def test_calls_set_factory_on_given_object(self):
        self.conf(self.manager)
        self.manager.set_factory.assert_called_with(IsA(type), \
                IsCallable())


if "__main__" == __name__:
    unittest.main()
