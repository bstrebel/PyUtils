#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging

def import_code(code, name, sys_module=False):
    import sys, imp
    module = imp.new_module(name)
    exec code in module.__dict__
    if sys_module:
        sys.modules[name] = module
    return module
