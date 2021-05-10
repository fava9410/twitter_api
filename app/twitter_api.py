from requests_oauthlib import OAuth1Session


class Twitter_API():

    def __init__(self,credentials):
        self.client_key = credentials['api_key']
        self.client_secret = credentials['api_secret_key']
        self.resource_owner_key = credentials['access_token']
        self.resource_owner_secret = credentials['access_token_secret']

        self.login()

    def login(self):

        self.twitter = OAuth1Session('KRy7l0v8wex3w8Sy5zThai3Ea',
                                    client_secret='X2eBm0Y21kYEuR74W3Frqc2JVIizOj8Q1EVGatDsEVVEJo0ucu',
                                    resource_owner_key='1220032047516921859-otvXjhExyUTZ5GLxssc9h5ORqtPZja',
                                    resource_owner_secret='tmJKqM4ORfQW6CH7wIVV8uKNpmSEmeFAP8lYwGb19uYjj')
    
    def last_5_tweets(self, screen_name):
        print("me llaman")
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {"screen_name": screen_name, "count": 5}
        
        r = self.twitter.get(url, params=params)

        tweets = []
        for tweet in r.json():
            tweets.append({"date": tweet['created_at'], 'text': tweet['text']})

        return tweets