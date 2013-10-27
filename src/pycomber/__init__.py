#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycomber.manager import Manager
from pycomber.configuration import ConfigurationNoneType, ConfigurationComplex,\
    ConfigurationPrimitives, ConfigurationAggregate


merger = Manager()
ConfigurationAggregate(ConfigurationComplex(), ConfigurationPrimitives(),
        ConfigurationNoneType())(merger)

__all__ = [merger]
