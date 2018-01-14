#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filename: rooms.py
Purpose: room route config file
"""

if __name__ == "__main__":
    print("This file is not meant to be executed directly.")
    import sys
    sys.exit(1)

def configuration(config):
    config.add_route("rooms",                    "/rooms")
    config.add_route("rooms_id",                 "/rooms/{id}")

