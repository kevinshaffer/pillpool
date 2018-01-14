#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filename: config.py
Purpose: Provides application config

"""

import os
import json
import base64
import netifaces
from Crypto.Cipher import AES

unpad = lambda s : s[0:-ord(s[-1])]

# These functions are copied from security.py to avoid circular imports

def config_value(path):
    parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return get_config_value("{}/config/config.json".format(parent), path)

def get_config_value(config_file, path, default=None):
    """ Internal function just to safely extract json values from config file """
    # Caller needs to handle any exceptions, not this method's job.
    with open(config_file, "r") as f:
        data = json.loads(f.read())
    return find(path, data)

def find(element, json_data, delimiter="/"):
    keys = element.split(delimiter)
    rv = json_data
    for key in keys:
        rv = rv[key]
    return json.dumps(rv)

def decrypt(enc, key = None):
    '''
    Decrypt packets sent from the front end.
    '''

    if key == None:
        key = CONNECTION_STRING_KEY

    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]).decode())


