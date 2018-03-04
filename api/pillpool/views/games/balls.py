from pyramid.view import view_config
from pillpool.lib.authentication import restricted
import pillpool.models.games.balls as balls
import pillpool.lib.util as util

@view_config(route_name="balls_id_pot", request_method="PUT", renderer="json")
@restricted()
def put_balls_id_pot(request):
    return balls.pot(
        room_id=request.matchdict["room_id"], 
        game_id=request.matchdict["game_id"], 
        ball_number=request.matchdict["ball_number"], 
        user_id=request.token["id"]
    )

@view_config(route_name="balls_id_unpot", request_method="PUT", renderer="json")
@restricted()
def put_balls_id_unpot(request):
    return balls.unpot(
        room_id=request.matchdict["room_id"], 
        game_id=request.matchdict["game_id"], 
        ball_number=request.matchdict["ball_number"], 
        user_id=request.token["id"]
    )

