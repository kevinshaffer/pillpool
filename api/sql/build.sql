drop schema pp cascade;
create schema pp;

create table if not exists pp.users(
	id serial
	, email text unique
	, username text
	, first_name text
	, last_name text
	, password text
	, salt text
	, temp text
	, photo bytea
	, guest boolean default false
    , room_id integer
	, date_created float default extract(epoch from now())
	, date_modified float
	, date_deleted float default null
	, primary key (id)
);

create table if not exists pp.friends(
	ID serial
	, user_one INTEGER --requester
	, user_two integer -- requestee
	, status text -- 'accepted','pending','rejected'
	, date_created float default extract(epoch from now())
	, date_modified float
	, date_deleted float default null
	, primary key (id)
);

create table if not exists pp.rooms(
	ID serial
	, owner_user_id INTEGER
	, name text
	, passphrase text
	, players integer[] default array[]::integer[]
	, private BOOLEAN
	, location jsonb
	, date_created float default extract(epoch from now())
	, date_modified float
	, date_deleted float default null
	, primary key (id)
);
create unique index on pp.rooms (name) where date_deleted is null and name is not null;
-- Unique room based on name and date_deleted is NULL

create table if not exists pp.games(
	ID serial
	, room_id INTEGER references pp.rooms(id)
	, winner integer -- references pp.users
	, players integer[] default array[]::integer[]
	, balls jsonb
	, date_created float default extract(epoch from now())
	, date_modified float
	, date_deleted float default null
	, primary key (id)
);

create table if not exists pp.room_names(
	name text not null,
	, free boolean default true,
    , date_selected float default null
	, primary key (animal)
);
/*
Balls: {
    "1": {
        "owner": 1,
        "state": "live",
        "clicker": 2
    },
    "2" : {
        
    }
}
*/


-- TODO: have a trigger for date modified on games/rooms?