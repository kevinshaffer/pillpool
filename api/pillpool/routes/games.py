#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filename: games.py
Purpose: game route config file
"""

if __name__ == "__main__":
    print("This file is not meant to be executed directly.")
    import sys
    sys.exit(1)

def configuration(config):
    config.add_route("games",           "/rooms/{room_id}/games")
    config.add_route("games_id",        "/rooms/{room_id}/games/{game_id}")
    config.add_route("games_id_leave",  "/rooms/{room_id}/games/{game_id}/leave")

    config.add_route("balls_id_pot",    "/rooms/{room_id}/games/{game_id}/balls/{ball_number}/pot")
    config.add_route("balls_id_unpot",  "/rooms/{room_id}/games/{game_id}/balls/{ball_number}/unpot")

