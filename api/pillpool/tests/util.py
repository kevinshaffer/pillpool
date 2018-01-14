# Standard Library Imports
import unittest
import json
import sys
import os

# Third Party Imports
import webtest
from pyramid import testing
from pyramid.httpexceptions import HTTPForbidden

def get_authorization_token(config_file_path="config.tests.json"):
    from pillpool.lib.authentication import login
    try:
        config = json.loads(open("pillpool/config/{}".format(config_file_path), "r").read())
        if "jwt" in config and config["jwt"]:
            return config["jwt"]
        elif "username" in config and "password" in config and config["username"] and config["password"]:
            import base64
            request = testing.DummyRequest()
            request.context = testing.DummyResource()
            username = config["username"]
            password = config["password"]
            request.authorization = ["Basic", base64.b64encode(str.encode('{}:{}'.format(username, password))).decode()]
            token_response = login(request)
            return token_response.body.decode()
    except:
       return None