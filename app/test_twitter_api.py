import unittest
import json
from twitter_api import Twitter_API

class TwitterApiTest(unittest.TestCase):

    def setUp(self):
        # load credentials
        with open('app/credentials.json') as f:
            credentials = json.load(f)

        twitter_credentials = credentials['twitter_api']

        self.twitter = Twitter_API(twitter_credentials)

    def test_last_5_tweets(self):
        response = self.twitter.last_5_tweets('eminem')

        self.assertEqual(len(response), 5)
    
    def test_last_5_tweets_return_nothing(self):
        response = self.twitter.last_5_tweets('noexistonoretornonada')

        self.assertTrue(response == [])
    
    def test_get_user_info(self):
        response = self.twitter.get_user_info('eminem')

        self.assertTrue('title' in response and 'image_url' in response)
    
    def test_get_user_info_return_empty_dict(self):
        response = self.twitter.get_user_info('noexistonoretornonada')

        self.assertTrue(response == {})

if __name__ == '__main__':
    unittest.main()