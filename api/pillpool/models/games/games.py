from pillpool.lib.connections import execute_query
from pillpool.models.rooms.rooms import get_room_id
import random
import json

EMOJIS = {
    0: ["&#x1F601", "&#x1F60E", "&#x1F914", "&#x1F636", "&#x1F643", "&#x1F631", "&#x1F922", "&#x1F608", "&#x1F921", "&#x1F63B", "&#x1F4A9", "&#x1F916", "&#x1F64A", "&#x1F47B", "&#x1F913"],
    1: ['&#x1F4A9', '&#x1F631', '&#x1F922', '&#x1F63B', '&#x1F914', '&#x1F608', '&#x1F601', '&#x1F636', '&#x1F60E', '&#x1F47B', '&#x1F916', '&#x1F921', '&#x1F913', '&#x1F643', '&#x1F64A'],
    2: ['&#x1F63B', '&#x1F631', '&#x1F914', '&#x1F608', '&#x1F636', '&#x1F47B', '&#x1F64A', '&#x1F921', '&#x1F643', '&#x1F601', '&#x1F60E', '&#x1F4A9', '&#x1F916', '&#x1F922', '&#x1F913'],
    3: ['&#x1F921', '&#x1F916', '&#x1F608', '&#x1F60E', '&#x1F636', '&#x1F922', '&#x1F914', '&#x1F601', '&#x1F631', '&#x1F4A9', '&#x1F913', '&#x1F63B', '&#x1F47B', '&#x1F64A', '&#x1F643'],
    4: ['&#x1F914', '&#x1F4A9', '&#x1F921', '&#x1F913', '&#x1F60E', '&#x1F64A', '&#x1F643', '&#x1F636', '&#x1F63B', '&#x1F922', '&#x1F916', '&#x1F608', '&#x1F631', '&#x1F601', '&#x1F47B'],
    5: ['&#x1F63B', '&#x1F47B', '&#x1F913', '&#x1F631', '&#x1F643', '&#x1F4A9', '&#x1F608', '&#x1F636', '&#x1F916', '&#x1F64A', '&#x1F922', '&#x1F601', '&#x1F921', '&#x1F914', '&#x1F60E'],
    6: ['&#x1F922', '&#x1F914', '&#x1F913', '&#x1F608', '&#x1F60E', '&#x1F916', '&#x1F47B', '&#x1F921', '&#x1F4A9', '&#x1F601', '&#x1F64A', '&#x1F643', '&#x1F636', '&#x1F631', '&#x1F63B'],
    7: ['&#x1F60E', '&#x1F913', '&#x1F636', '&#x1F4A9', '&#x1F916', '&#x1F608', '&#x1F64A', '&#x1F47B', '&#x1F631', '&#x1F643', '&#x1F922', '&#x1F63B', '&#x1F921', '&#x1F601', '&#x1F914'],
    8: ['&#x1F636', '&#x1F922', '&#x1F64A', '&#x1F913', '&#x1F4A9', '&#x1F608', '&#x1F921', '&#x1F601', '&#x1F916', '&#x1F63B', '&#x1F643', '&#x1F631', '&#x1F914', '&#x1F60E', '&#x1F47B'],
    9: ['&#x1F913', '&#x1F63B', '&#x1F60E', '&#x1F636', '&#x1F47B', '&#x1F921', '&#x1F922', '&#x1F914', '&#x1F64A', '&#x1F4A9', '&#x1F608', '&#x1F916', '&#x1F643', '&#x1F601', '&#x1F631']
}

# Start gamme
def post_games(room_id, user_id, balls_per_player):
    room_id = get_room_id(room_id)
    game_already_running_query = "select id from pp.games where room_id = %s and winner is null;"
    game_already_running_result = execute_query(
        datasource="db/pillpool",
        query=game_already_running_query,
        db_params=[room_id]
    )
    if game_already_running_result:
        return {"status_code": 404, "error": True, "message": "This room already has a running game.", "game_id": game_already_running_result[0]["id"], "parameter": None}
    query = """
        INSERT into pp.games (
            room_id
            , players
        ) select
            r.id
            , r.players
        from pp.rooms r
        where r.id = %s
            and %s = ANY(r.players)
            and not exists(select 1 from pp.games where room_id = r.id and winner is null)
        returning id, players
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[room_id, user_id]
    )
    if result:
        game_id = result[0]["id"]
        players = result[0]["players"]

        # Randomly assign the balls to players
        players_by_balls = players * balls_per_player
        balls = dict((el,{"player": None, "state": "live", "potted_by": None, "date_potted": None}) for el in range(1,16))
        balls_remaining = list(balls.keys())
        random.shuffle(balls_remaining)
        for player in players_by_balls:
            ball = balls_remaining.pop()
            balls[ball]["player"] = player

        query = """
            UPDATE pp.games
                set balls = %s
            where id = %s
            returning id
        """
        result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[json.dumps(balls), game_id]
    )
        return get_games_id(room_id, game_id, user_id)
    else:
        return {"status_code": 404, "error": True, "message": "This room does not exist."}

# TODO: This needs to return an object that says how many balls each player has left
# I don't think I need the ball_hash anymore... but maybe?
def get_games_id(room_id, game_id, user_id, last_modified=None):
    room_id = get_room_id(room_id)
    query = """
        SELECT
            g.id
            , g.winner
            , u.username as winner_username
            , (select json_object_agg(id, json_build_object('emoji', null, 'username',username,'balls_remaining',0, 'balls', '[]'::jsonb)) from pp.users where id = ANY(g.players)) as players
            , g.balls
            , digest(g.balls::text::bytea, 'sha256')::text as ball_hash
            , g.date_created
            , g.date_modified
            , coalesce((round(g.date_modified::numeric, 2) > round(%s::numeric, 2)),False) as send_response
        from pp.games g
        inner join pp.rooms r
            on r.id = g.room_id
        left join pp.users u
            on u.id = g.winner
        where r.id = %s
            and g.id = %s
            and %s = ANY(r.players)
            and g.date_deleted is null;
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[last_modified, room_id, game_id, user_id]
    )
    my_balls = []
    remaining_players = []
    if result:
        if last_modified and not result[0]["send_response"]:
            return {"status_code": 204}
        else:
            del result[0]["send_response"]
        # TODO: Need to process the balls object, to obfuscate who owns each ball before returning it to the client side.
        for ball_number, ball_info in result[0]["balls"].items():
            
            ball_owner = ball_info["player"]

            # See how many are left per player
            if ball_info["state"] == "live" and ball_owner:
                result[0]["players"][str(ball_owner)]["balls_remaining"] += 1
                """ This makes the balls appear in the list for you, maybe want to disable this if it's confusing? """
                if int(ball_owner) == user_id:
                    result[0]["players"][str(ball_owner)]["balls"].append(int(ball_number))
                else:
                    result[0]["players"][str(ball_owner)]["balls"].append(None)

                if ball_owner not in remaining_players:
                    remaining_players.append(ball_owner)
            elif ball_owner and ball_info["state"] == "potted":
                result[0]["players"][str(ball_owner)]["balls"].append(int(ball_number))

            # Aggregate what balls are left for me
            if ball_owner == user_id:
                my_balls.append(int(ball_number))
                
            # Remove information about who has each ball
            del result[0]["balls"][ball_number]["player"]

        result[0]["my_balls"] = my_balls
        result[0]["remaining_players"] = remaining_players
        for i, player_id in enumerate(sorted(result[0]["players"])):
            result[0]["players"][player_id]["emoji"] = EMOJIS[int(room_id)%len(EMOJIS)][i]
        return result[0]
    else:
        return  {"status_code": 404, "error": True, "message": "This game does not exist."}

def get_games(room_id, user_id):
    room_id = get_room_id(room_id)
    query = """
        SELECT
            g.id
            , g.winner
            , u.username as winner_username
            , (select username from pp.users where id = ANY(g.players))
            , g.date_created
            , g.date_modified
        from pp.games g
        inner join pp.rooms r
            on r.id = g.room_id
        left join pp.users u
            on u.id = g.winner
        where r.id = %s
            and %s = ANY(r.players)
            and g.date_deleted is null;
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[room_id, user_id]
    )
    return result


def leave(room_id, game_id, user_id):
    room_id = get_room_id(room_id)
    query = """
        UPDATE pp.games
            set players = array_remove(players, %s)
        where id = %s
            and room_id = %s
        returning id
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id, game_id, room_id]
    )
    return True

