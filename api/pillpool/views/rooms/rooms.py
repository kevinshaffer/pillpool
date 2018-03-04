from pyramid.view import view_config
from pyramid.response import Response
from pillpool.lib.authentication import restricted
import pillpool.models.rooms.rooms as rooms
import pillpool.lib.util as util

@view_config(route_name="rooms", request_method="POST", renderer="json")
@restricted()
def post_rooms(request):
    try:
        j = request.json
    except:
        j = {}
    return rooms.post_rooms(
        user_id=request.token["id"],
        name=util.get_value(j, "name"),
        passphrase=util.get_value(j, "passphrase"),
        location=util.get_value(j, "location")
    )

@view_config(route_name="rooms", request_method="GET", renderer="json")
@restricted()
def get_rooms(request):
    return rooms.get_rooms(request.token["id"])

@view_config(route_name="rooms_id", request_method="GET", renderer="json")
@restricted()
def get_rooms_id(request):
    response = rooms.get_rooms_id(
        room_id=request.matchdict["room_id"], 
        user_id=request.token["id"], 
        last_modified=util.get_value(request.params.mixed(), "last_modified")
    )
    if not response:
        return Response(status_code=404,json={"message": "Room does not exist"})
    else:
        return response

@view_config(route_name="rooms_id_live_game", request_method="GET", renderer="json")
@restricted()
def get_rooms_id_live_game(request):
    return rooms.get_rooms_id_live_game(
        room_id=request.matchdict["room_id"], 
        user_id=request.token["id"]
    )

@view_config(route_name="rooms_id_join", request_method="POST", renderer="json")
@restricted()
def post_rooms_id_join(request):
    return rooms.join(request.matchdict["room_id"], request.token["id"])

@view_config(route_name="rooms_id_leave", request_method="POST", renderer="json")
@restricted()
def post_rooms_id_leave(request):
    return rooms.leave(request.matchdict["room_id"], request.token["id"])
