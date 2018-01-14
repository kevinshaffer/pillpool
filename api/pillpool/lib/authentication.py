# Standard Library Imports
import functools
import base64
import json
import os
# Third Party Imports
from pyramid.httpexceptions import HTTPForbidden, HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config
import jwt
import logging
# Local Imports
from pillpool.lib.connections import execute_query
from pillpool.lib.config import config_value, get_config_value

SECRET = config_value("keys/jwt")
ISSUER = config_value("keys/jwt-issuer")

"""
Structure of authentication
    Login:
        Request:
            Basic Auth Username/Password
            Authorization Token (JWT)
            Form Username/Password
            JSON Username/Password
        Response:
            200:
                Authorization Bearer Token
            403:
                Invalid Username or Password.
                Username or password not valid.
                No valid authorization detected.

    Restricted Endpoint:
        Request:
            Basic Auth Username/Password
            Authorization Token (JWT)

        Response:
            200:
                Whatever the endpoint is to return
            403:
                Invalid Username or Password.
                Username or password not valid.
                No valid authorization detected.
"""

@view_config(route_name="login", request_method="POST", renderer="json")
def login(request):
    """
    Validates user login and responds with a Json Web Token if successful

    Parameters:
        username (str, optional): username to log in with
        password (str, optional): password to log in with

    Response:
        200: Authorization Token
        403: Invalid Username or Password.

    """
    if request.authorization:
        validate_authorization(request)
        token = request.token
    else:
        try:
            credentials = request.json
        except:
            credentials = dict(request.POST.items())

        validate_login_schema(credentials["username"], credentials["password"])

        token = validate_credentials(credentials["username"], credentials["password"])

    # Token is JWT object
    token["iss"] = ISSUER
    encoded = jwt.encode(token, SECRET, algorithm="HS256")

    response = Response(encoded.decode("utf-8"))
    response.content_type = "application/jwt"
    return response


def restricted():
    """
    Checks for a valid authentication token/schema
    """
    def _dec(f):
        @functools.wraps(f)
        def wrapper(request):
            try:
                validate_authorization(request)
            # any exception indicates that the authorization process has failed.
            except Exception as e:
                raise HTTPForbidden("No valid authorization detected.")
            return f(request)
        return wrapper
    return _dec

def decode_jwt(request):
    """
    Subroutine used to retrieve decoded jwt from
    request object.
    Leave this out in order to aid unit testing.
    """
    auth = request.authorization[1]

    # The options are bypassing a security feature, but I couldn"t figure it out otherwise.
    return jwt.decode(auth, key=SECRET, options={"verify_aud":False})

def validate_credentials(email, password):
    """
    Validates email and password against database returning a token dictionary.

        Parameters:
            email (str): email to log in with
            password (str): Password to log in with

        Response:
            token (dict): Dictionary token (JWT)
    """
    try:
        query = """
            SELECT
                u.id
                , u.email
                , u.first_name
                , u.last_name
            from pp.users u
            where u.email = %s
                and u.date_deleted is null
                and u.temp is null
                and encode(digest(%s||u.salt, 'sha256'), 'hex')=u.password;
        """
        result = execute_query(
            datasource="db/pillpool",
            query=query,
            db_params=[email,password]
        )
        if result:
            return result[0]
        else:
            raise HTTPForbidden("Invalid Username or Password.")
    except:
        raise HTTPForbidden("Invalid Username or Password.")

def validate_authorization(request):
    """
    Validates request authorization tokens to see if it is authorized with this instance of the API.

        Parameters:
            request (object): Request object from Pyramid Framework

        Response:
            200: None
            403: No valid authorization detected.
    """
    if request.authorization:
        if request.authorization[0] == "Basic":
            validate_basic_auth(request)
        elif request.authorization[0] == "Bearer":
            validate_bearer(request)
        else:
            raise HTTPForbidden("No valid authorization detected.")
    else:
        raise HTTPForbidden("No valid authorization detected.")

def validate_basic_auth(request):
    """
    Validates basic authorization key to see if it is authorized with this instance of the API.

        Parameters:
            request (object): Request object from Pyramid Framework

        Response:
            200: None
            403: Invalid Username or Password.
    """
    username, password = base64.b64decode(request.authorization[1]).decode("utf-8").split(":")
    token = validate_credentials(username, password)
    if not token:
        raise HTTPForbidden("Invalid Username or Password.")
    request.token = token


def validate_bearer(request):
    """
    Validates bearer authorization token to see if it is authorized with this instance of the API.

        Parameters:
            request (object): Request object from Pyramid Framework

        Response:
            200: None
            403: No valid authorization detected.
    """
    token = decode_jwt(request)
    request.token = token
    if(token["iss"] != ISSUER):
        raise HTTPForbidden("No valid authorization detected.")

def validate_login_schema(username, password):
    """
    Validates login schema to make sure username and password are strings of certain sizes

    Parameters:
        username (str): Username to log in with
        password (str): Password to log in with

    Response:
        200: None
        400: Invalid Username or Password
    """
    if not (type(username) == str and type(password) == str and len(username) <= 254):
        raise HTTPBadRequest("Username or password not valid.")