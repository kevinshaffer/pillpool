from pillpool.lib.connections import execute_query
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

def post_rooms(user_id, name=None, passphrase=None, location=None):
    exists = False
    if name:
        exists = execute_query(
            datasource="db/pillpool",
            query="select exists(select 1 from pp.rooms where name = %s and date_deleted is null and name is not null)",
            db_params=[name]
        )[0]
    if exists:
        return [{"error": True, "message": "A room with this name already exists, try another name", "parameter": None}]

    query = """
        INSERT into pp.rooms(
            owner_user_id
            , name
            , passphrase
            , location
        )
        VALUES(
            %s
            , %s
            , %s
            , %s
        ) returning id
    """
    room_id = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id, name, passphrase, location]
    )[0]["id"]
    join(room_id, user_id)
    if not name:
        execute_query(
            datasource="db/pillpool",
            query="update pp.rooms set name = id where id = %s",
            db_params=[room_id],
            output_type="raw"
        )
        name = room_id
    return {"name": name, "id": room_id}


def get_rooms_id(room_id, user_id, last_modified = None):
    query = """
        SELECT
            r.id
            , r.owner_user_id
            , u.first_name as owner_first_name
            , u.last_name as owner_last_name
            , r.name
            , r.location
            , u.email
            , u.photo
            , (select json_object_agg(id, json_build_object('username',username,'emoji',null)) from pp.users where id = ANY(r.players)) as players
            , (select g.id from pp.games g where room_id = r.id and date_deleted is null and winner is null order by id desc limit 1) as game_id
        from pp.rooms r
        left join pp.users u
            on u.id = r.owner_user_id
        where r.id = %s
            and %s = ANY(r.players)
            and r.date_deleted is null
            and (r.date_modified > %s) is not False;
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[room_id, user_id, last_modified]
    )
    if result:
        for i, player_id in enumerate(sorted(result[0]["players"])):
            result[0]["players"][player_id]["emoji"] = EMOJIS[int(room_id)%9][i]
        return result[0]
    else:
        return {}

def get_rooms_id_live_game(room_id, user_id):
    query = """
        select 
            g.id as game_id 
        from pp.games g 
        where room_id = %s 
            and date_deleted is null 
            and winner is null 
        order by id desc limit 1
            and %s = ANY(players)
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[room_id, user_id]
    )
    if result:
        return result[0]
    else:
        return {"game_id": None}

def get_rooms(user_id):
    query = """
        SELECT
            r.id
            , r.owner_user_id
            , u.username as owner_username
            , r.name
            , r.location
        from pp.rooms r
        left join pp.users u
            on u.id = r.owner_user_id
        where (r.owner_user_id = %s or %s=ANY(players))
            and r.date_deleted is null;
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id, user_id]
    )
    return result

def join(room_id, user_id):
    # If player is in a different room, remove them:
    query = """
        UPDATE pp.rooms r
            set players = array_remove(players, u.room_id)
        from (
            select room_id from pp.users where id = %s
        ) u
        where r.id = u.room_id
        returning id;
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id]
    )

    # Add player to new room
    query = """
        UPDATE pp.rooms
            set players = array_append(players, %s)
        where id = %s
            and (not (%s = ANY(players)) or players is null)
        returning id
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id, room_id, user_id]
    )

    # Update player's room_id so we know where they are
    query = """
        UPDATE pp.users
            set room_id = %s
        where id = %s
        returning id
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[room_id, user_id]
    )
    return True

def leave(room_id, user_id):
    query = """
        UPDATE pp.rooms
            set players = array_remove(players, %s)
        where id = %s
        returning id
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id, room_id]
    )
    query = """
        UPDATE pp.users
            set room_id = null
        where id = %s
        returning id
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id]
    )
    return True