from pillpool.lib.connections import execute_query, execute_stored_procedure

def post_users(username, email=None, password=None, first_name=None, last_name=None):
    result = execute_stored_procedure(
        datasource="db/pillpool",
        name="pp.create_user",
        parameters={
            "p_username":username,
            "p_email":email,
            "p_password":password,
            "p_first_name":first_name,
            "p_last_name":last_name
        }
    )
    return get_users_id(result[0]["create_user"])

def get_users_id(user_id):
    query = """
        SELECT
            u.id
            , json_build_object(
                'id', u.id,
                'username', u.username,
                'first', u.first_name,
                'last', u.last_name,
                'email', u.email,
                'photo', u.photo,
                'guest', u.guest
            ) as user
        from pp.users u
        where id = %s
    """
    result = execute_query(
        datasource="db/pillpool",
        query=query,
        db_params=[user_id]
    )
    return result[0]