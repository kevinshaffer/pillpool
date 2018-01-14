# Testing

## Running Tests
Running tests is very simple.
1. Copy [this file](../config/config.tests.default.json) to `/timeseries/config/config.tests.json`, and fill out the credentials. (It will default to using a jwt if you have one there, so don't fill it out if it is not valid)
    1.  `jwt` is if you already have a validated `jwt` to use.
    2.  `username` is your DCL username
    3.  `password` is your DCL password
2. Navigate to the top level of this repository and run the command: `docker-compose -f docker-compose.test.yml up`

### Notes:
1. All tests that are created need to be in the `timeseries/tests` directory. 
2. If the test is a function it must end in `_test` to be picked up by the test runner, and if it's a class it must end in `Test`.

## Utilities
The file `util.py` is a test utility that houses some helper functions, one of which returns a valid authorization token from the file: `timeseries/config/config.tests.json`.

It is also useful to import a few modules and instantiate them as global variables, which you'll see in the examples below.
These include:
1. `webtest.TestApp(timeseries.main({}))`
2. `unittest.TestCase()` 
3. `pyramid.testing.setUp()`


## Sample Tests

### Webtest Testapp Methodology
This test utilizes the [webtest.TestApp](https://docs.pylonsproject.org/projects/webtest/en/latest/api.html) module. This means you can make get/post/put/delete/etc requests to endpoints by url. You can also pass in parameters, expected status codes, and more. 

The sample functions below are hitting a dummy endpoint /test with a POST request and expects a 2xx response. Which then is checked to see if there is a JSON/dictionary response with a key of `message`

#### Basic Example
```python
# Imports
import json
import unittest
import webtest

# These are defined globally since most functions will use them.
Test = unittest.TestCase()
TestApp = webtest.TestApp(timeseries.main({}))
def webtest_testapp_test():
    url = "/test"
    parameters = {
        "param_1": 1,
        "param_2": [1,2,3],
        "param_3": {"foo": "bar"}
    }
    expected_status = "2*"
    # Make requst to the url in question
    response = TestApp.post(
        url = url,
        params = json.dumps(parameters),
        status = expected_status
    )
    # Test to see if `message` is in the response
    Test.assertTrue("message" in response)
```
#### Authorization Example
```python
# Imports
import json
import unittest
import webtest
import timeseries.tests.util as util

# These are defined globally since most functions will use them.
Test = unittest.TestCase()
TestApp = webtest.TestApp(timeseries.main({}))
TOKEN = util.get_authorization_token()
AUTH_HEADER = {"Authorization": "Bearer {}".format(TOKEN)}
def authorized_webtest_testapp_test():
    url = "/test_with_authorization"
    parameters = {
        "param_1": 1,
        "param_2": [1,2,3],
        "param_3": {"foo": "bar"}
    }
    expected_status = "2*"
    # Make requst to the url in question
    response = TestApp.post(
        url = url,
        params = json.dumps(parameters),
        status = expected_status,
        # Add headers
        headers = AUTH_HEADER
    )
    # Test to see if `message` is in the response
    Test.assertTrue("message" in response)
```


### Pyramid Testing Methodology
This test utilizes the [pyramid.testing](https://docs.pylonsproject.org/projects/pyramid/en/latest/api/testing.html) module. This means you can build request objects, which are what the functions used in the API expect, and therefore you can import and call those functions directly. 


The sample functions below are hitting a dummy function `test`. Which then is checked to see if there is a dictionary response with a key of `message`.

*Note: These functions cannot determine the response status of the call, since they're just hitting a function, rather than having that function interpretted by the framework into a request object. However: If the function returns a Response object, then you could.*
#### Basic Example
```python
# Imports
import unittest
import pyramid

# This is defined globally since most functions will use it.
Test = unittest.TestCase()
def pyramid_testing_example():
    from timeseries.views import test_function

    parameters = {
        "param_1": 1,
        "param_2": [1,2,3],
        "param_3": {"foo": "bar"}
    }

    # Build dummy request object
    request = pyramid.testing.DummyRequest()
    request.context = pyramid.testing.DummyResource()

    # Add parameters as POST variables to request object
    request.POST = parameters

    # Make request to the function in question
    response = test_function(request)
    
    # Test to see if `message` is in the response
    Test.assertTrue("message" in response)
```

#### Authorization Example:
```python
# Imports
import timeseries.tests.util as util
import unittest
import pyramid

# Global variables since most functions will use them.
Test = unittest.TestCase()
TOKEN = util.get_authorization_token()
AUTHORIZATION = ["Bearer", TOKEN]
def authorized_pyramid_testing_example():
    from timeseries.views import test_function_with_authorization

    parameters = {
        "param_1": 1,
        "param_2": [1,2,3],
        "param_3": {"foo": "bar"}
    }

    # Build dummy request object
    request = pyramid.testing.DummyRequest()
    request.context = pyramid.testing.DummyResource()

    # Add parameters as POST variables to request object
    request.POST = parameters

    # Add Bearer authorization to request
    request.authorization = AUTHORIZATION

    # Make request to the function in question
    response = test_function_with_authorization(request)
    
    # Test to see if `message` is in the response
    Test.assertTrue("message" in response)
```
