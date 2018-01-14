from pyramid.view import view_config
from pillpool.lib.authentication import restricted
import pillpool.models.users.users as users

@view_config(route_name="users_id", request_method="GET", renderer="json")
@restricted()
def get_users_id(request):
    if request.matchdict["id"] == "me":
        _id = request.token["id"]
    else:
        _id = request.matchdict["id"]
    return users.get_users_id(_id)