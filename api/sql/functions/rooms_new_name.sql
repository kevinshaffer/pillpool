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