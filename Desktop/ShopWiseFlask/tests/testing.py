 
import requests
import requests_mock
import unittest


session = requests.Session()
adapter = requests_mock.Adapter()
session.mount('mock', adapter)

adapter.register_uri('GET', 'http://localhost:9000/ ')
resp = session.get("http://localhost:9000/")
print resp.status_code

    
    