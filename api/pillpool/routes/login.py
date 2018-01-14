#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filename: login.py
Purpose: login route config file
"""

if __name__ == "__main__":
    print("This file is not meant to be executed directly.")
    import sys
    sys.exit(1)

def configuration(config):
    config.add_route('login', '/login')

