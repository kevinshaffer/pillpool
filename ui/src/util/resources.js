
import requestPromiseNative from 'request-promise-native';
import jwtDecode from 'jwt-decode';
var config = require('./config.json');

let apiPrefix = config.apiPrefix;// || 'http://localhost:6540';


function getToken() {
    let token = localStorage.getItem('token');
    if (token == null) {
        return dataResource.payload = null;
    }
    dataResource.API = requestPromiseNative.defaults({
        baseUrl: apiPrefix,
        headers: {Authorization: 'Bearer ' + token},
        json: true,
        resolveWithFullResponse: true
    });
    dataResource.payload = jwtDecode(token);
    return token;
}

function setToken(token) {
    localStorage.setItem('token', token);
}
function clearToken(){
    localStorage.removeItem('token');
}

// Allow other modules to use this function to redirect back after a login
function forceLogin(path) {
    clearToken();
    location.href = "/";
    throw new Error('Not Authenticated');
}

var dataResource = {
    API: null,
    getToken,
    setToken,
    clearToken,
    payload: null,
    forceLogin,
    apiPrefix: apiPrefix
};

export default dataResource;
