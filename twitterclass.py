from urllib.parse import scheme_chars
import tweepy
import datetime
import hmac
import json
from time import time
from hashlib import sha512
import requests


class Main:
    tweetstatus = False

    def __init__(self, taccount, keyword, key, secret, cointype, amount, amounttype, endDate, startDate):
        #Twitter conditions
        self.taccount = taccount
        self.keyword = keyword

        #Coinspot API keys
        self.key = key
        self.secret = secret
        #Coinspot conditions
        self.cointype = cointype
        self.amount = amount 
        self.amounttype = amounttype

        #Time
        self.endDate = endDate
        self.startDate = startDate

    def check_tweet(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        global tweetstatus
        tmpTweets = api.user_timeline(self.taccount, tweet_mode="extended", count=1)
        if tmpTweets == []:
            print("@" + self.taccount + " has no tweets")
        else:
            for tweet in tmpTweets: #For each individual tweet in tmptweets
                if self.startDate <= tweet.created_at <= self.endDate:
                    print("Tweet was uploaded recently")
                    if self.keyword in tweet.full_text:
                        print(self.keyword + " was found in the tweet")
                        Main.tweetstatus = True
                    elif self.keyword not in tweet.full_text:
                        print(self.keyword + " was not found")
                        Main.tweetstatus = False
                else:
                    print("No Tweet in the last" + " 6 " + "seconds")
                    Main.tweetstatus = False


    def chunker(self, data):
        yield data 

    def request(self, path, data=None):
        API_ENDPOINT = "https://www.coinspot.com.au/api/v2"
        if data is None:
            data = {}

        data["nonce"] = int(time() * 1000)
        json_data = json.dumps(data, separators=(',', ':')).encode()

        return requests.post(
            API_ENDPOINT + path,
            data= self.chunker(json_data),
            headers={
                "Content-Type": "application/json",
                "sign": hmac.new(secret, json_data, sha512).hexdigest(),
                "key": key,
            }
        ).json()
        

    def buy(self):
        return self.request("/my/buy/now", {
            "cointype": self.cointype,
            "amount": self.amount,
            "amounttype": self.amounttype,
            }) 
    






