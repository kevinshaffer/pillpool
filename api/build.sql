create extension pgcrypto;
create schema auth;
create table auth.users(
	id serial
	, email text unique
	, first_name text
	, last_name text
	, password text
	, salt text
	, temp text default null
	, date_created float default extract(epoch from now())
	, date_modified float default null
	, date_deleted float default null
	, primary key (id)
);
drop function auth.create_user(text,text,text,text,text[]);
CREATE OR REPLACE FUNCTION auth.create_user(
    p_email text
    , p_password text
    , p_first_name text DEFAULT NULL::text
    , p_last_name text DEFAULT NULL::text
    --, p_permissions text[] DEFAULT NULL::text[]
)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
declare
    v_salt text;
    v_salted_pw text;
    --v_permission text;
    v_user_id integer;
begin
    select gen_salt('bf') into v_salt;
    select encode(digest(p_password||v_salt, 'sha256'), 'hex') into v_salted_pw;

    insert into auth.users (email, password, salt, first_name, last_name)
        values (p_email, v_salted_pw, v_salt, p_first_name, p_last_name)
    returning id into v_user_id;

    -- if p_permissions is not null then
    --     foreach v_permission in array p_permissions loop
    --         if v_permission in ('admin') then
    --             insert into auth.permissions(role, permission) values (v_role_id, v_permission);
    --         end if;
    --     end loop;
    -- end if;

    return v_user_id;

end
$function$;

select auth.create_user('kevinshaffera@gmail.com', 'test', 'Kevin', 'Shaffer')
;

select * from auth.users;


                    SELECT
                        id
                    from auth.users u
                    where u.email = 'kevinshaffera@gmail.com'
                        and u.date_deleted is null
                        and u.temp is null
                        and encode(digest('test'||u.salt, 'sha256'), 'hex')=u.password;