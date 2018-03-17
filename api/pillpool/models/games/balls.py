from pillpool.lib.connections import execute_query
import pillpool.models.games.games as games
from pillpool.models.rooms.rooms import get_room_id


# Check to see if there is only one remaining player
def check_game_over(room_id, game_id, game_info):
    room_id = get_room_id(room_id)
    if len(game_info["remaining_players"]) == 1:
        winner_id, winner_username = set_winner(room_id, game_id, game_info["remaining_players"][0])
        game_info["winner"] = winner_id
        game_info["winner_username"] = winner_username
    
# Set the winner variable in the games record
def set_winner(room_id, game_id, player_id):
    room_id = get_room_id(room_id)
    query = """
        UPDATE pp.games
            set winner = %s
        where id = %s
            and room_id = %s
            and winner is null
        returning id;
        """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[player_id, game_id, room_id]
    )
    winner = "select username from pp.users where id = %s"
    winner_name = execute_query(
        datasource="db/pillpool",
        query=winner,
        db_params=[player_id]
    )[0]["username"]
    return player_id, winner_name


def pot(room_id, game_id, ball_number, user_id, potter_user_id=None):
    room_id = get_room_id(room_id)
    query = """
        UPDATE pp.games
            set balls = jsonb_set(
                balls
                , '{%s}'
                , jsonb_build_object(
                    'state', 'potted',
                    'potted_by', %s,
                    'date_potted', extract(epoch from now()),
                    'player', balls->'%s'->'player'
                )
            )
        where id = %s
            and room_id = %s
            and %s = ANY(players)
        returning id, balls
    """
    if potter_user_id == None:
        potter_user_id = user_id
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[int(ball_number), potter_user_id, int(ball_number), game_id, room_id, user_id]
    )
    game_info = games.get_games_id(room_id, game_id, user_id)
    check_game_over(room_id, game_id, game_info)
    print(game_info)
    return game_info

def unpot(room_id, game_id, ball_number, user_id):
    room_id = get_room_id(room_id)
    query = """
        UPDATE pp.games
            set balls = jsonb_set(
                balls
                , '{%s}'
                , jsonb_build_object(
                    'state', 'live',
                    'potted_by', null,
                    'date_potted', null,
                    'player', balls->'%s'->'player'
                )
            )
        where id = %s
            and room_id = %s
            and %s = ANY(players)
        returning id
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[int(ball_number), int(ball_number), game_id, room_id, user_id]
    )

    return games.get_games_id(room_id, game_id, user_id)