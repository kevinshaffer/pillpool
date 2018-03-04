#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filename: main.py
Purpose: main route config file
"""

if __name__ == "__main__":
    print("This file is not meant to be executed directly.")
    import sys
    sys.exit(1)

import pillpool.routes.login      as login_configuration
import pillpool.routes.rooms      as rooms_configuration
import pillpool.routes.games      as games_configuration
import pillpool.routes.users      as users_configuration

def main(config):
    login_configuration.configuration(config)
    rooms_configuration.configuration(config)
    games_configuration.configuration(config)
    users_configuration.configuration(config)

