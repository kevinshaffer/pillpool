# Standard Library Imports
import unittest
import json
import sys
import os

# Third Party Imports
import webtest
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

def get_customers_test():
    res = TestApp.get(
        url='/scada/customers', 
        headers=AUTH_HEADER,
        status='2*'
    )