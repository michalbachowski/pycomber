#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycomber.manager import Manager
from pycomber.configuration import ConfigurationDefault


merger = Manager()
ConfigurationDefault()(merger)

__all__ = [merger]
