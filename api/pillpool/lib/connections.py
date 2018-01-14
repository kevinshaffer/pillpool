#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filename: connections.py
Purpose: Provides connections to database from SQLAlchemy pools.

"""
import json
import logging  # Logging has been disabled in this module for now by Wendy.
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from pillpool.lib.config import config_value
from pillpool.lib.util import get_value
import threading

"""
Connections to Athena
    Reference: https://github.com/laughingman7743/PyAthena
"""
ENGINES_LOCK = threading.Lock() # use a lock to ensure that we don't get two threads trying to mutate the EXISTING_ENGINES at any one time
EXISTING_ENGINES = {}  # Holds url:engine pairs.
KNOWN_CONFIG = {}
KNOWN_HOST_IDS = {} # mapping from host ID to connection string

def get_connection_url(datasource={"key": "db/pillpool"}):
    if get_value(datasource, "key") == "db/athena":
        return get_athena_connection_url(datasource)
    elif get_value(datasource, "type") == "athena":
            return get_athena_connection_url(datasource)
    config_key = datasource["key"]
    if config_key not in KNOWN_CONFIG.keys():
        KNOWN_CONFIG[config_key] = json.loads(config_value(config_key))
    return "postgresql://{username}:{password}@{host}:{port}/{database}".format(**KNOWN_CONFIG[config_key])

def get_athena_connection_url(datasource):
    config_key=get_value(datasource, "key", "db/athena")
    if config_key not in KNOWN_CONFIG.keys():
        KNOWN_CONFIG[config_key] = json.loads(config_value(config_key))
    database_name=get_value(datasource, "database_name", "acciona")
    s3_dir=get_value(datasource, "s3_dir", "pillpool-json-fs/acciona-backup-pillpool/companies/acciona/")
    region_name=get_value(datasource, "region_name", get_value(KNOWN_CONFIG[config_key], "aws_region_name", "us-east-1"))
    return 'awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}@athena.{region_name}.amazonaws.com:443/{database_name}?s3_staging_dir={s3_staging_dir}'.format(
        aws_access_key_id=quote_plus(KNOWN_CONFIG[config_key]["aws_access_key_id"]),
        aws_secret_access_key=quote_plus(KNOWN_CONFIG[config_key]["aws_secret_access_key"]),
        region_name=region_name,
        database_name=database_name,
        s3_staging_dir=quote_plus('s3://{}'.format(s3_dir))
    )

def get_connection(url):
    ENGINES_LOCK.acquire()
    try:
        if url in EXISTING_ENGINES.keys():
            engine = EXISTING_ENGINES[url]
        else:
            engine = create_engine(url)
            EXISTING_ENGINES[url] = engine
    finally:
        ENGINES_LOCK.release()

    return engine.connect()

# Useful if you have an endpoint with lots of queries.
def get_connection_object(database="db/pillpool", database_name=None, s3_dir=None, region_name=None):
    connection_url = get_connection_url(config_key=database, database_name=database_name, s3_dir=s3_dir, region_name=region_name)
    return get_connection(connection_url).execution_options(autocommit=True)


def execute_query(query="", db_params=[], sql_type='table', output_type='json', datasource="db/pillpool", connection=None):
    if type(datasource) == str:
        datasource = {"key": datasource}
    if not query:
        raise Exception('Query text is required.')
    if not connection:
        connection_url = get_connection_url(datasource)
        conn = get_connection(connection_url).execution_options(autocommit=True)
    else:
        conn = connection

    if type(db_params) == str:
        db_params = [db_params]

    if output_type == 'raw':
        if type(db_params) == dict:
            raw = conn.execute(query, **db_params)
        else:
            result = conn.execute(query, *db_params)
        if not connection: conn.close()
        return result
    else: # For now we're outputting json only
        if sql_type == 'table' or sql_type == 'table-denormalized':
            if type(db_params) == dict:
                result_raw = conn.execute(query, **db_params)
            else:
                result_raw = conn.execute(query, *db_params)
            columns = result_raw.keys()
            result = [dict(zip(columns,row)) for row in result_raw]
            if not connection: conn.close()
            return result
        elif sql_type == 'table-normalized':
            if type(db_params) == dict:
                result_q = conn.execute(query, **db_params)
            else:
                result_q = conn.execute(query, *db_params)
            columns = result_q.keys()
            result = [list(i) for i in result_q]
            if not connection: conn.close()
            return {"columns":columns, "rows": result}
        elif sql_type == 'json':
            try:
                if type(db_params) == dict:
                    result = json.loads(conn.execute(query, **db_params).fetchall()[0][0])
                else:
                    result = json.loads(conn.execute(query, *db_params).fetchall()[0][0])
            except KeyError:
                result = json.loads('[]')
            if not connection: conn.close()
            return result
        else: # Return raw result object
            if type(db_params) == dict:
                result = conn.execute(query, **db_params)
            else:
                result = conn.execute(query, *db_params)
            if not connection: conn.close()
            return result

def execute_stored_procedure(name="", parameters=[], sql_type='table', output_type='json', datasource="db/pillpool", connection=None):
    if type(datasource) == str:
        datasource = {"key": datasource}
    if not name:
        raise Exception("Name is required.")
    if parameters:
        if type(parameters) is list:
            # This requires the parameters to be in the correct order
            param_string = "%s," * len(parameters)
            param_string = param_string[:-1]
            param_content = parameters
        elif type(parameters) is dict:
            # This requires the named parameters to be what the database expects.
            raw_list = [(k, v) for k, v in parameters.items()]
            # Format pairs from parameters dict to appear in the same order in string and contents.
            param_string = ', '.join(["%s:=?" % (p[0]) for p in raw_list])
            param_string = param_string.replace('?', "%s")
            param_content = [p[1] for p in raw_list]
        else:
            raise Exception("parameters for database must be sent as dict or list, can be empty")
    else:
        param_string = ""
        param_content = []
    query = "select * from %s"%(name)
    return execute_query(query + '(' + param_string + ');',
                        param_content,
                        sql_type,
                        output_type,
                        datasource,
                        connection)


# Use for queries that return table structures (but return denormalized)
def execute_query_table(conn, query):
    result_q = conn.execute(query);
    columns = result_q.keys()
    result = [dict(zip(columns,row)) for row in result_q]
    conn.close()
    return result

# Use for queries that return table structures (but return normalized)
def execute_query_table_normalized(conn, query):
    result_q = conn.execute(query);
    columns = result_q.keys()
    result = [list(i) for i in result_q]
    conn.close()
    return {"columns":columns, "rows": result}

# Use for queries that return table json
def execute_query_json(conn, query):
    try:
        result = json.loads(conn.execute(query).fetchall()[0][0]);
    except KeyError:
        result = json.loads('[]')
    conn.close()
    return result