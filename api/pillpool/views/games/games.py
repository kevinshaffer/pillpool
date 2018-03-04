from pyramid.view import view_config
from pyramid.response import Response
from pillpool.lib.authentication import restricted
import pillpool.models.games.games as games
import pillpool.lib.util as util

@view_config(route_name="games", request_method="POST", renderer="json")
@restricted()
def post_games(request):
    balls_per_player = util.get_value(request.json, "balls", 3)
    response = games.post_games(
        room_id=request.matchdict["room_id"],
        user_id=request.token["id"],
        balls_per_player=balls_per_player
    )
    if "error" in response:
        if response["error"]:
            return Response(status_code=response["status_code"], json=response)
    return response

@view_config(route_name="games", request_method="GET", renderer="json")
@restricted()
def get_games(request):
    return games.get_games(request.matchdict["room_id"], request.token["id"])

@view_config(route_name="games_id", request_method="GET", renderer="json")
@restricted()
def get_games_id(request):
    response = games.get_games_id(
        room_id=request.matchdict["room_id"], 
        game_id=request.matchdict["game_id"], 
        user_id=request.token["id"], 
        last_modified=util.get_value(request.params.mixed(), "last_modified")
    )
    if not response:
        return Response(status_code=404,json={"message": "Game does not exist"})
    else:
        if "error" in response:
            if response["error"]:
                return Response(status_code=response["status_code"], json=response)
        elif "status_code" in response:
            if response["status_code"] == 204:
                return Response(status_code=204)
        return response

@view_config(route_name="games_id_leave", request_method="POST", renderer="json")
@restricted()
def post_games_id_leave(request):
    return games.leave(request.matchdict["room_id"], request.matchdict["game_id"], request.token["id"])
