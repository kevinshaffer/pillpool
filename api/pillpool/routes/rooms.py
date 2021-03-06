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
    config.add_route("rooms_id",                 "/rooms/{room_id}")
    config.add_route("rooms_id_live_game",       "/rooms/{room_id}/games/live")
    config.add_route("rooms_id_join",            "/rooms/{room_id}/join")
    config.add_route("rooms_id_leave",           "/rooms/{room_id}/leave")