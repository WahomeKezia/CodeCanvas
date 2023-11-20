import unittest
from flask import Flask, session
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_code_input_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Paste Your Code here', response.data)

    def test_save_code(self):
        response = self.app.post('/save_code', data={'code': 'print("Hello, World!")'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(session['code'], 'print("Hello, World!")')

    def test_reset_session(self):
        with app.test_request_context('/reset_session', method='POST'):
            session['code'] = 'print("Hello, World!")'
            response = app.full_dispatch_request()
            self.assertEqual(response.status_code, 302)  # Redirect status code
            self.assertNotIn('code', session)

    def test_style_page(self):
        response = self.app.get('/style')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Select Your Style', response.data)

    def test_save_style(self):
        response = self.app.post('/save_style', data={'style': 'monokai', 'code': 'print("Hello, World!")', 'language': 'python'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(session['style'], 'monokai')
        self.assertEqual(session['code'], 'print("Hello, World!")')

    def test_image_page(self):
        response = self.app.get('/image')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Done!', response.data)

    # Add more test cases as needed for your application

if __name__ == '__main__':
    unittest.main()
