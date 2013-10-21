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
