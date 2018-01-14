from pillpool.lib.connections import execute_query

# TODO: This query needs to be able to validate whether or not you're in the room
def get_rooms_id(user_id, room_id):
    query = """
        SELECT
            r.id
            , r.owner_user_id
            , u.first_name as owner_first_name
            , u.last_name as owner_last_name
            , r.name
            , r.location
            , r.email
            , r.photo
        from pp.rooms r
        left join pp.users u
            on u.id = r.owner_user_id
        where (not r.private or r.owner_user_id = %s)
            and r.id = %s
            and r.date_deleted is null;
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id, room_id]
    )
    if result:
        return result[0]
    else:
        return {}

def get_rooms(user_id):
    query = """
        SELECT
            r.id
            , r.owner_user_id
            , u.first_name as owner_first_name
            , u.last_name as owner_last_name
            , r.name
            , r.location
            , u.email
        from pp.rooms r
        left join pp.users u
            on u.id = r.owner_user_id
        where (not r.private or r.owner_user_id = %s)
            and r.date_deleted is null;
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id]
    )
    return result