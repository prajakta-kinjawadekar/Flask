
import os
import shopwise
import unittest
import tempfile
from flask import Flask


class ShopWiseTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
	    ''' To create mock database connection '''
	    cls.db_fd, shopwise.app.config['DATABASE'] = tempfile.mkstemp()
	    shopwise.app.testing = True
	    cls.app = shopwise.app.test_client()
	    with shopwise.app.app_context():
	        shopwise.init_db()
			
			
    @classmethod	
    def tearDownClass(cls):
	    ''' To close the database connection '''
	    os.close(cls.db_fd)
	    os.unlink(shopwise.app.config['DATABASE'])
	
	
    def test_homepage(self):
	    ''' Test case to check homepage '''
	    rv = self.app.get('/')
	    self.assertEqual(rv.status_code, 200)


    def register(self, firstname, lastname, username, password):   
        return self.app.post('/register', data=dict(
		    firstname = firstname,
			lastname = lastname,
            username=username,
            password=password
        ), follow_redirects=True)
	
	
    def test_register(self):
	    ''' Test case to check registration of new User '''
	    rv = self.register('Aarti', 'Walimbe', 'aa', 'aa')
	    self.assertEqual(rv.status_code, 200)
	
	
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
	
	
    def test_login(self):
	    ''' Test case to check successful login of User '''
	    rv = self.register('Prajakta', 'kinjawadekar', 'aa', 'aa')
	    rv1 = self.login('aa', 'aa')
	    self.assertEqual(rv1.status_code, 200)
	
	
    def postAd(self, title, category, price, name, mobile, email, address):
        return self.app.post('/postAd', data=dict(
            title = title,
            category = category, 
            price = price,
		    name = name,
		    mobile = mobile,
		    email = email,
		    address = address    
        ), follow_redirects=True)
	
	
    def test_postAd(self):
	    ''' Test case to check successful posting of ad by User '''
	    rv = self.register('Aarti', 'Walimbe', 'aa', 'aa')
	    rv = self.login('aa', 'aa')
	    rv1 = self.postAd('aa', 'Cars', 67, 'gfygdu', 89578598, 'fuis@gmail', 'gr' )
	    self.assertEqual(rv1.status_code, 200)
	
	
if __name__ == '__main__':
    unittest.main()
  
    