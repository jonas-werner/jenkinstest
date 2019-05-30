import os
import unittest
import myapp
import pytest

class MyTestCase(unittest.TestCase):

    def setUp(self):
        myapp.app.testing = True
        self.app = myapp.app.test_client()

    def tearDown(self):
		pass

    def test_mainmenu(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EVENT SURVEY - Jenkins - try 2', response.data)
    #
    # def test_agenda(self):
    #     response = self.app.get('/agenda', follow_redirects=True)
    #     assert b'DevOps demystified' in response.data
    #     assert b'Login' not in response.data
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'DevOps demystified', response.data)
    #     self.assertNotIn(b'Login', response.data)
    #
    # def test_survey(self):
    #     response = self.app.get('/survey', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'EVENT SURVEY', response.data)
    #     self.assertIn(b'Division', response.data)
    #     self.assertIn(b'State', response.data)
    #     self.assertIn(b'SUBMIT', response.data)
    #
    # def test_create_survey(self):
    #     response = self.app.post('/suthankyou.html', data=dict(
	# 		division='Enterprise',
	# 		state='NSW',
	# 		feedback='Facemeltingly Awesome'
	# 	), follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'THANKS FOR TAKING THE SURVEY', response.data)
    #
    # def test_survey_dump(self):
    #     response = self.app.get('/dumpsurveys', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Division : Enterprise', response.data)
    #     self.assertIn(b'State    : NSW', response.data)
    #     self.assertIn(b'Feedback : Facemeltingly Awesome', response.data)

# Method	Equivalent to
# .assertEqual(a, b)	a == b
# .assertTrue(x)	bool(x) is True
# .assertFalse(x)	bool(x) is False
# .assertIs(a, b)	a is b
# .assertIsNone(x)	x is None
# .assertIn(a, b)	a in b
# .assertIsInstance(a, b)	isinstance(a, b)
# .assertIs(), .assertIsNone(), .assertIn(), and .assertIsInstance() all have opposite methods, named .assertIsNot(), and so forth.

if __name__ == '__main__':
    unittest.main()
