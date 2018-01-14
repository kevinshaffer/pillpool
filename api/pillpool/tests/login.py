# Standard Library Imports
import unittest
import json
import sys
import os

# Third Party Imports
import webtest
from pyramid import testing
from pyramid.httpexceptions import HTTPForbidden

# Local Imports
import pillpool
import pillpool.tests.util as util

# Global Variables used for most tests
Test = unittest.TestCase()
TestApp = webtest.TestApp(pillpool.main({}))
TOKEN = util.get_authorization_token()
AUTH_HEADER = {"Authorization": "Bearer {}".format(TOKEN)}
AUTHORIZATION = ["Bearer", TOKEN]

testing.setUp()
def login_success_jwt_test():
    res = TestApp.post(
        url='/login',
        headers=AUTH_HEADER,
        status='2*'
    )
    Test.assertTrue(str(res.body))

def login_failure_test():
    res = TestApp.post(
        url='/login',
        params=json.dumps({"username": "bad_username", "password": "really_bad_password"}),
        status='4*'
    )

def login_failure_basic_test():
    from pillpool.lib.authentication import login
    request = testing.DummyRequest()
    request.authorization = ["Basic", "YmFkX3VzZXJuYW1lOnJlYWxseV9iYWRfcGFzc3dvcmQ="]
    request.context = testing.DummyResource()
    Test.assertRaises(HTTPForbidden, login, request)

def login_failure_basic_2_test():
    res = TestApp.post(
        url='/login',
        headers={"Authorization": "Basic YmFkX3VzZXJuYW1lOnJlYWxseV9iYWRfcGFzc3dvcmQ="},
        status='4*'
    )

testing.tearDown()