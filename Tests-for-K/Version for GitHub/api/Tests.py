import requests
import pytest


browser_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/113.0'}


def test_code_200():
    r = requests.get('http://ipinfo.io/8.8.8.8/json')
    assert r.status_code == 200


def test_https():
    r = requests.get('https://ipinfo.io/8.8.8.8/json')
    assert r.status_code == 200


def test_IPv6():
    r_IPv6 = requests.get('http://ipinfo.io/2001:4860:4860::8888/json')
    assert r_IPv6.status_code == 200
    assert r_IPv6.json().get('ip') == '2001:4860:4860::8888'


def test_head_metod():
    r = requests.head('http://ipinfo.io/2001:4860:4860::8888/json')
    headers = r.headers.keys()
    assert r.status_code == 200
    assert len(r.content) == 0
    assert'access-control-allow-origin' in headers
    assert'x-frame-options' in headers
    assert'x-xss-protection' in headers
    assert'x-content-type-options' in headers
    assert'referrer-policy' in headers
    assert'content-type' in headers
    assert'content-length' in headers
    assert'date' in headers
    assert'strict-transport-security' in headers
    assert'vary' in headers
    assert'Via' in headers


def test_options_metod():
    r = requests.options('http://ipinfo.io/2001:4860:4860::8888/json')
    assert r.status_code == 204
    assert r.headers.get('access-control-allow-methods') == 'GET,HEAD,PUT,PATCH,POST,DELETE'


def test_get_details():
    r = requests.get('http://ipinfo.io/54.246.228.58/json')
    assert r.status_code == 200
    r = r.json()
    assert r.get("ip") == "54.246.228.58"
    assert r.get("hostname") == "ec2-54-246-228-58.eu-west-1.compute.amazonaws.com"
    assert r.get("city") == "Dublin"
    assert r.get("region") == "Leinster"
    assert r.get("country") == "IE"
    assert r.get("loc") == "53.3331,-6.2489"
    assert r.get("org") == "AS16509 Amazon.com, Inc."
    assert r.get("postal") == "D02"
    assert r.get("timezone") == "Europe/Dublin"


def test_request_with_filter_param():
    r = requests.get('http://ipinfo.io/54.246.228.58/org')
    assert r.status_code == 200
    # В запросе с фильтрацией, api возвращает 'plaintext', а не JSON
    assert r.text.replace('\n', '') == 'AS16509 Amazon.com, Inc.'


def test_request_with_browser_headers():
    r = requests.get('http://ipinfo.io/8.8.8.8', headers=browser_headers)
    assert r.status_code == 200
    assert '<!DOCTYPE html>' in r.text


def test_wrong_token():
    r = requests.get('http://ipinfo.io/8.8.8.8?token=123WrongToken321')
    assert r.status_code == 403
    assert r.json().get('error').get('title') == 'Unknown token'


def test_json_before_ip():
    r = requests.get('http://ipinfo.io/json/8.8.8.8')
    assert r.status_code == 404


def test_filter_param_before_ip():
    r = requests.get('http://ipinfo.io/hostname/8.8.8.8')
    assert r.status_code == 404


def test_ip_zero():
    r = requests.get('http://ipinfo.io/0')
    assert r.status_code == 404


def test_negative_ip():
    r = requests.get('http://ipinfo.io/-8.8.8.8')
    assert r.status_code == 404


def test_caps_json():
    r = requests.get('http://ipinfo.io/8.8.8.8/JSON')
    assert r.status_code == 400
    assert r.json().get('error').get('title') == 'Wrong module or field type'


def test_caps_filter_param():
    r = requests.get('http://ipinfo.io/8.8.8.8/IP')
    assert r.status_code == 400
    assert r.json().get('error').get('title') == 'Wrong module or field type'


def test_asn_data_access_with_free_plan():
    r = requests.get('http://ipinfo.io/8.8.8.8/asn')
    assert r.status_code == 400
    assert r.json().get('error').get('message') == 'Please pass a valid token to access \'asn\' module.'


def test_ip_address_with_comma():
    r = requests.get('http://ipinfo.io/8,8,8,8/')
    assert r.status_code == 404
    assert r.json().get('error').get('title') == 'Wrong ip'


def test_simplest_sql_injection():
    r = requests.get('http://ipinfo.io/8.8.8.8\' OR 1=1--')
    assert r.status_code == 404
    assert r.json().get('error').get('title') == 'Wrong ip'

