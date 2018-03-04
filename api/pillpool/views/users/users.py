import jwt

# Third Party
from pyramid.response import Response
from pyramid.view import view_config

# Local
from pillpool.lib.authentication import restricted
import pillpool.models.users.users as users
from pillpool.lib.config import config_value, get_config_value

SECRET = config_value("keys/jwt")
ISSUER = config_value("keys/jwt-issuer")

# Need endpoint to convert temporary user to full account.

@view_config(route_name="users", request_method="POST", renderer="json")
def post_users(request):
    token = users.post_users(**request.json)

    # Token is JWT object
    token["iss"] = ISSUER
    encoded = jwt.encode(token, SECRET, algorithm="HS256")

    response = Response(encoded.decode("utf-8"))
    response.content_type = "application/jwt"
    return response


@view_config(route_name="users_id", request_method="GET", renderer="json")
@restricted()
def get_users_id(request):
    if request.matchdict["id"] == "me":
        _id = request.token["id"]
    else:
        _id = request.matchdict["id"]
    return users.get_users_id(_id)