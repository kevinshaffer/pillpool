from pyramid.view import view_config
from pillpool.lib.authentication import restricted
import pillpool.models.rooms.rooms as rooms

@view_config(route_name="rooms", request_method="GET", renderer="json")
@restricted()
def get_rooms(request):
    return rooms.get_rooms(request.token["id"])

@view_config(route_name="rooms_id", request_method="GET", renderer="json")
@restricted()
def get_rooms_id(request):
    return rooms.get_rooms_id(request.matchdict["id"])