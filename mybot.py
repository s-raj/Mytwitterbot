#!/usr/bin/env python
import tweepy
from threading import Thread
from keys import *
from config import *
import sys
import os
import time
from time import sleep
from random import random
from random import randrange
from datetime import datetime, timedelta
from threading import Timer

# your twitter consumer and access information goes here
CONSUMER_KEY = keys['apiKey']
CONSUMER_SECRET = keys['apiSecret']
ACCESS_TOKEN = keys['accessToken']
ACCESS_TOKEN_SECRET = keys['accessTokenSecret']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Create API object
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
  def __init__(self, api):
        self.api = api
        self.me = api.me()
  def on_status(self, tweet):
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                #tweet.retweet()
                print(tweet.text)		
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

  def on_error(self, status_code):
     print("Error detected")
     if status_code == 420:
       #returning False in on_data disconnects the stream
       if (LOGLVL >= 0):
         print("Stream Disconnected")
       return False

def verifyauth():
  global api
  try:
    api.verify_credentials()
    print("Authentication OK")
  except:
    print("Error during authentication")

def replyDirectMsg():
  print ("Reply direct message")
  global api
  verifyauth()
  currenttimestamp = 1591563577493
  while True:
     try:
       last_dms = api.list_direct_messages(1)
       #print(last_dms)
       for messages in last_dms:
         if (int(messages.created_timestamp) > int(currenttimestamp)) :
            currenttimestamp = int(messages.created_timestamp)
            print(messages.message_create['message_data']['text'])
            message = "Hello, This is an automated reply. Will get back to you soon! Regards Sharat " + str(currenttimestamp)
            senderid = messages.message_create['sender_id']
            if (senderid != TWITTER_SENDER_ID):
              api.send_direct_message(senderid, message)
     except:
       if(LOGLVL >= 0):
          print("TWITTER BOT: Unexpected Error" , sys.exc_info()[0])
     finally:
       if(LOGLVL >= 2):
         print("TWITTER BOT: Executed replyDirectMsg thread")
       sleep(60 * 60/DM_POLL_FREQ_IN_HOUR)


def random_line(fileName, default=None):
    line = default
    for i, randomline in enumerate(fileName, start=1):
        if randrange(i) == 0:  # random int [0..i)
            line = randomline
    return line

def randomTweet():
  print ("Random Tweet")
  global api
  verifyauth()
  while True:
    try:
      startTime = datetime.today()
      nextTweet = startTime.replace(day = startTime.day, hour = RANDOM_TWEET_HOUR, minute = RANDOM_TWEET_MINUTE, second = RANDOM_TWEET_SEC, microsecond = RANDOM_TWEET_MSEC) + timedelta(days=RANDOM_TWEET_DAYS)
      deltaTime = nextTweet - startTime
      sleepTime = deltaTime.total_seconds()
      
      with open(os.path.join(os.path.dirname(__file__), RANDOM_TWEET_TXT_FILE)) as file:
        line =  random_line(file)
        if(LOGLVL >= 2):
          print("TWITTER BOT: random quote at {0}: ".format(startTime) + line)
        api.update_status(str(line))
    except :
      if(LOGLVL >= 0):
        print("TWITTER BOT: Oops! Something went wrong! {0}".format(err))

    finally:
      if (LOGLVL >= 2):
         print("TWITTER BOT: randomTweet send!")
      sleep(sleepTime)

def handleTweetMentions():
  print("Handle tweet mentions")
  global api
  myStreamListener = MyStreamListener(api)
  myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener(api))
  myStream.filter(track=['@__SHARATRAJ__'])
  print ("TWITTER BOT: Stream object created. ")


def main():
  handleTweetThread = Thread(target=handleTweetMentions)
  handleTweetThread.start()

  randomTweetThread = Thread(target=randomTweet)
  randomTweetThread.start()

  replyDirMsgThread = Thread(target=replyDirectMsg)
  replyDirMsgThread.start()

  '''
  End of execution... Join threads
  '''
  handleTweetThread.join()
  randomTweetThread.join()
  replyDirMsgThread.join()

if __name__=='__main__':
  main()
  #done
