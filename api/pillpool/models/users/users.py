from pillpool.lib.connections import execute_query

def get_users_id(user_id):
    query = """
        SELECT
            id
            , first_name
            , last_name
            , email
            , photo
        from pp.users
        where id = %s
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id]
    )
    return result[0]