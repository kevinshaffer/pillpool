#!/usr/bin/python
# -*- coding: utf-8 -*-
# Standard Library Imports
# Third Party Imports
# Local Imports

def get_value(obj,name,defValue=None):
    if name in obj:
        if obj[name] != None:
            if obj[name] == '':
                return defValue
            return obj[name]

    return defValue