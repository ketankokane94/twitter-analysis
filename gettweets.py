import tweepy
import csv


class dealWithTwitter:
    def __init__(self):
        self.access_token = ""
        self.access_token_secret = ""
        self.consumer_key = ""
        self.consumer_secret = ""
        self.api = ""

    def loadTokens(self):
        tokens = []
        with open('pwd.txt') as pwd_file:
            for line in pwd_file:
                tokens.append(line.strip())
                print(line.strip())
        self.access_key = tokens[0]
        self.access_secret = tokens[1]
        self.consumer_key = tokens[2]
        self.consumer_secret = tokens[3]


    def get_all_tweets(self, screen_name):
        # Twitter only allows access to a users most recent 3240 tweets with this method
        self.loadTokens()
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(auth)
        # initialize a list to hold all the tweepy Tweets
        alltweets = []
        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.api.user_timeline(screen_name=screen_name, count=200)
        # save most recent tweets
        alltweets.extend(new_tweets)
        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))
            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
            # save most recent tweets
            alltweets.extend(new_tweets)
            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            print("...%s tweets downloaded so far" % (len(alltweets)))
        # transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
        # write the csv
        try:
            with open('%s_tweets.csv' % screen_name, 'wb') as f:
                writer = csv.writer(f)
                writer.writerow(["id".encode(), "created_at".encode(), "text".encode()])
                writer.writerows(outtweets)
        except:
            pass


if __name__ == '__main__':
    t = dealWithTwitter()
    t.loadTokens()
    t.get_all_tweets('realDonaldTrump')
    # t.connectToTwitter()
