from urllib.parse import scheme_chars
import tweepy
import datetime
import time

second = 1

consumer_key = "BvGNCWzUYH6AJhQHK42XZ1D6f"
consumer_secret = "gwewwo32qQhpp9FE6QT20n7lxJHwsU5pg2MDkVwh1xbiXcAaJn"
access_key = "825202212712247296-kBzdx3t1F8ogSpxN6d8weEvyzwDOj1L"
access_secret = "UJZzvqL8gFeRmDuha2gZxMoAYJZCWEVhjeUJCLPgl2sxV"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

username = "jack_bialek"
tweets = []
tmpTweets = api.user_timeline(username, tweet_mode="extended")


startDate= datetime.datetime.now()
hours_added = datetime.timedelta(hours = second)
endDate = startDate + hours_added

for tweet in tmpTweets: #For each individual tweet in tmptweets
    print(tweet.full_text) #Print Tweet in full text`
    if tweet.created_at < endDate and tweet.created_at > startDate: #If the tweet is created in the last hour
        tweets.append(tweet) #Add tweet to Tweets list



response = coinspot.latest("BTC")
    print(response)
    session["api_key"] = api_key
    session["secret_key"] = api_secret
    response = coinspot.my_balances()
    print(response)
    response = coinspot.my_balance("AUD")
    print(response)
    response = coinspot.my_deposit()
    print(response)
