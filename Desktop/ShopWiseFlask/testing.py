 
import requests
import requests_mock
from unittest import TestCase
import unittest

class Testing(TestCase):
    @requests_mock.mock()
    def test_checkHomePage(self,m):
        m.get("http://localhost:9000/")
        self.assertEquals(requests.get("http://localhost:9000/").status_code,200)

if __name__ == '__main__':
    unittest.main()

  
    