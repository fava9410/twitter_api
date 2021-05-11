import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db, Portfolio, portfolio_schema_tweets
import json

class AppTest(TestCase):

    # I used a local db to unit tests, I was afraid of use Zemoga's connection for that, in cause you want to run unit tests,
    # please create another database and modify "SQLALCHEMY_DATABASE_URI" with the required data.

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/zemoga_test_db"
    TESTING = True

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI

        return app

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        
        db.init_app(app)
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Deletes databases once testing is finished
        """
        db.session.remove()
        db.drop_all()

    def create_user_test(self, twitter_user='test_twitter', 
                        name_user='name_test', lastname_user='lastname_test'):
        new_port = Portfolio(twitter_user, name_user, lastname_user)
        db.session.add(new_port)
        db.session.commit()
    
    def test_users_method_not_allowed(self):
        tester = app.test_client(self)
        response = tester.post('/users')
        self.assertEqual(response.status_code, 405)
        response = tester.put('/users')
        self.assertEqual(response.status_code, 405)
        response = tester.delete('/users')
        self.assertEqual(response.status_code, 405)
    
    def test_user_method_not_allowed(self):
        tester = app.test_client(self)
        response = tester.post('/user/1')
        self.assertEqual(response.status_code, 405)
        response = tester.put('/user/1')
        self.assertEqual(response.status_code, 405)
        response = tester.delete('/user/1')
        self.assertEqual(response.status_code, 405)
    
    def test_create_user_method_not_allowed(self):
        tester = app.test_client(self)
        response = tester.get('/create_user')
        self.assertEqual(response.status_code, 405)
        response = tester.put('/create_user')
        self.assertEqual(response.status_code, 405)
        response = tester.delete('/create_user')
        self.assertEqual(response.status_code, 405)
    
    def test_delete_user_method_not_allowed(self):
        tester = app.test_client(self)
        response = tester.get('/delete_user/1')
        self.assertEqual(response.status_code, 405)
        response = tester.put('/delete_user/1')
        self.assertEqual(response.status_code, 405)
        response = tester.post('/delete_user/1')
        self.assertEqual(response.status_code, 405)
    
    def test_get_users_ok(self):
        tester = app.test_client(self)
        response = tester.get('/users')

        self.assertEqual(response.status_code, 200)
    
    def test_get_users_content(self):
        tester = app.test_client(self)
        response = tester.get('/users')

        self.assertEqual(response.content_type, 'application/json')
    
    def test_get_users_data_empty(self):
        tester = app.test_client(self)
        response = tester.get('/users')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, [])
    
    def test_get_users_data(self):
        tester = app.test_client(self)
        self.create_user_test()
        response = tester.get('/users')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'twitter_user_name' in response.data)
    
    def test_get_users_data_no_tweets(self):
        tester = app.test_client(self)
        self.create_user_test(twitter_user='eminem')
        response = tester.get('/users')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(b'tweets' in response.data)
    
    def test_get_user_not_found(self):
        tester = app.test_client(self)
        response = tester.get('/user/1')

        self.assertEqual(response.status_code, 404)
    
    def test_get_user(self):
        tester = app.test_client(self)
        self.create_user_test()
        response = tester.get('/user/1')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'twitter_user' in response.data)
    
    def test_get_user_empty_tweets(self):
        tester = app.test_client(self)
        self.create_user_test()
        response = tester.get('/user/1')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['tweets'], [])
    
    def test_get_user_with_5_tweets(self):
        tester = app.test_client(self)
        self.create_user_test(twitter_user='eminem')
        response = tester.get('/user/1')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['tweets']), 5)
    
    def test_delete_user(self):
        tester = app.test_client(self)
        self.create_user_test()
        response = tester.delete('/delete_user/1')

        self.assertEqual(response.status_code, 200)
    
    def test_delete_user_who_doesnt_exist(self):
        tester = app.test_client(self)
        self.create_user_test()
        response = tester.delete('/delete_user/55')

        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        tester = app.test_client(self)
        response = tester.post('/create_user', 
            data=dict(names='name_test', last_names='lastname_test', twitter_user='test_twitter'))
        
        self.assertEqual(response.status_code, 200)
    
    def test_create_user_missed_parameters(self):
        tester = app.test_client(self)
        response = tester.post('/create_user', 
            data=dict(names='name_test'))
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_get_user_info_from_twitter(self):
        tester = app.test_client(self)
        response = tester.post('/create_user', 
            data=dict(names='name_test', last_names='lastname_test', twitter_user='eminem'))

        portfolio = Portfolio.query.get_or_404(1)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(portfolio.title != None)
    
    def test_update_user(self):
        tester = app.test_client(self)
        self.create_user_test()
        user_created = Portfolio.query.get_or_404(1)
        last_names = user_created.last_names

        response = tester.put('/update_user/1', 
            data=dict(names='name_test', last_names='hola_mundo', twitter_user='test_twitter'))

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.get_data(as_text=True))

        self.assertNotEqual(last_names, response_json['last_names'])
    
    def test_update_user_who_doesnt_exits(self):
        tester = app.test_client(self)
        response = tester.put('/update_user/1', 
            data=dict(names='name_test', last_names='hola_mundo', twitter_user='test_twitter'))
        
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()