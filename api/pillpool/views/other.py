from pyramid.view import view_config
from pillpool.lib.authentication import restricted
from pillpool.lib.connections import execute_query

@view_config(route_name="sleep", request_method="GET", renderer="json")
def sleep(request):
    from time import sleep as sl
    if "seconds" in request.GET:
        sl(int(request.GET["seconds"]))
    else:
        sl(5)

@view_config(route_name="test",  renderer="json")
def test(request):
    return {"message": "hello"}
    
@view_config(route_name="test2", renderer="json")
@restricted()
def test2(request):
    return request.token

@view_config(route_name="db_test", renderer="json")
def scada_sample(request):
    try:
        limit = int(request.GET["limit"])
        if limit > 5:
            limit = 5
    except:
        limit = 5
    query = """
        SELECT
            *
        from dev.metrics
        limit %s;
    """
    result = execute_query(
        datasource="db/scada",
        query=query,
        db_params=[limit]
    )

    return {"result": result}

@view_config(route_name="athena", renderer="json")
def athena(request):
    try:
        limit = int(request.GET["limit"])
        if limit > 5:
            limit = 5
    except:
        limit = 5
    query = """
        SELECT
            *
        from acciona.acciona
        limit %(limit)s;
    """
    result = execute_query(
        datasource={"type": "athena", "key": "db/athena", "region_name": "us-east-1", "database_name": "acciona", "s3_dir": "scada-json-fs/acciona-backup-scada/companies/acciona"},
        query=query,
        db_params={"limit": limit}
    )
    return {"result": result}