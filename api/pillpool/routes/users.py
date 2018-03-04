#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filename: users.py
Purpose: user route config file
"""

if __name__ == "__main__":
    print("This file is not meant to be executed directly.")
    import sys
    sys.exit(1)

def configuration(config):
    config.add_route("users",                       "/users")
    config.add_route("users_id",                    "/users/{id}")

