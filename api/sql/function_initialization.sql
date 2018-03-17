CREATE OR REPLACE FUNCTION pp.create_user(
    p_username text
    , p_email text default null::text
    , p_password text default null::text
    , p_first_name text DEFAULT NULL::text
    , p_last_name text DEFAULT NULL::text
)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
declare
    v_salt text;
    v_salted_pw text;
    v_user_id integer;
    v_guest boolean default false;
begin

    if p_email is null then 
        v_guest := true;
        insert into pp.users(username, guest)
        VALUES(p_username, v_guest)
        returning id into v_user_id;
    else 
        select gen_salt('bf') into v_salt;
        select encode(digest(p_password||v_salt, 'sha256'), 'hex') into v_salted_pw;

        insert into pp.users (email, username, password, salt, first_name, last_name)
            values (p_email, p_username, v_salted_pw, v_salt, p_first_name, p_last_name)
        returning id into v_user_id;
    end if;

    return v_user_id;

end
$function$;

CREATE OR REPLACE FUNCTION rooms_new_name()
  RETURNS TRIGGER
  LANGUAGE plpgsql
AS $$
DECLARE
    v_name text;
BEGIN
    if NEW.name is null then
        update pp.room_names n
            set free = false
                , date_selected = extract(epoch from now())
        from (
            SELECT 
                name 
            FROM pp.room_names
            where free = true
            ORDER BY RANDOM()
            LIMIT 1
        ) rn
        where rn.name = n.name
        returning n.name into v_name;
        if v_name is null THEN
            
            update pp.room_names n
                set free = false
                    , date_selected = extract(epoch from now())
            from (
                SELECT 
                    name 
                FROM pp.room_names
                ORDER BY date_selected asc
                LIMIT 1
            ) rn
            where rn.name = n.name
            returning n.name into v_name;

            update pp.rooms
                set name = id
            where name = v_name;

        end if;

        NEW.name = v_name;

    end if;

    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION set_updated_timestamp()
  RETURNS TRIGGER
  LANGUAGE plpgsql
AS $$
BEGIN
  NEW.date_modified := extract(epoch from now());
  RETURN NEW;
END;
$$;