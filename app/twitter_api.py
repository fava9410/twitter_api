from requests_oauthlib import OAuth1Session


class Twitter_API():

    def __init__(self,credentials):

        self.twitter = OAuth1Session(credentials['api_key'],
                                    client_secret=credentials['api_secret_key'],
                                    resource_owner_key=credentials['access_token'],
                                    resource_owner_secret=credentials['access_token_secret'])
    
    def last_5_tweets(self, screen_name):

        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {"screen_name": screen_name, "count": 5}
        
        r = self.twitter.get(url, params=params)

        tweets = []

        if r.ok:
            for tweet in r.json():
                tweets.append({"date": tweet['created_at'], 'text': tweet['text']})

        return tweets
    
    def get_user_info(self, screen_name):

        url = "https://api.twitter.com/1.1/users/show.json"
        params = {"screen_name": screen_name}

        r = self.twitter.get(url, params=params)

        user_info = {}
        if r.ok:
            r_json = r.json()
            user_info = {"title": r_json['name'], "image_url": r_json['profile_image_url_https'], "description": r_json['description']}

        return user_info
