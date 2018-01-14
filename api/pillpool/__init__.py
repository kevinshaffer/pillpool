from pyramid.config import Configurator
from wsgicors import CORS

import pillpool.routes.main as routes

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    # Load in all the routes from the routes directory.
    routes.main(config)

    # One off endpoints
    config.add_route("sleep",   "/sleep")
    config.add_route("test",    "/test")
    config.add_route("test2",   "/test2")
    config.add_route("db_test", "/db_test")
    config.add_route("athena",  "/athena")
    config.scan()

    return CORS(config.make_wsgi_app(), headers="*", methods="*", maxage="180", origin="*")

