from flask_testing import TestCase
from flask import current_app, url_for
from main import app

class MainTest(TestCase):
    
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app
    
    def test_app_exist(self):
        self.assertIsNotNone(current_app)
        
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])
        
    def test_index_redirects(self):
        response = self.client.get(url_for('home'))
        self.assertRedirects(response, url_for('hello_world'))
        
    def test_hello_get(self):
        response = self.client.get(url_for('hello_world'))
        self.assert200(response)
        
    def test_helo_post(self):
        #fake_form = {
        #    'username': 'fake',
        #    'password': 'fake_password'
        #}
        response = self.client.post(url_for('hello_world'))
        self.assertTrue(response.status_code, 405)
        
    def test_auth_blueprint_exist(self):
        self.assertIn('auth', self.app.blueprints)
        
    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)
        
    def test_auth_login_render_form(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('auth/login.html')
        
    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake_password'
        }
        
        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('hello_world'))