from twython import Twython
from twython import TwythonStreamer
import random
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
import os
import time
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            tweettext = str(data['text'])
            user = str(data['user']['screen_name'])
            twitter = Twython(consumer_key, consumer_secret,access_token, access_token_secret)
            message = '@' + user +" Hi There! " + data['created_at']
            if (user == 'SharatRaj7'):
               #print("This is sharat's tweet")
               if tweettext.find('CMD_CORETEMP') != -1 :
                 temp = os.popen("vcgencmd measure_temp").readline() 
                 message = '@' + user + temp
               elif tweettext.find('CMD_RANDOMTWEET') != -1 :
                 filename = open('/home/pi/Documents/Myjobs/Mytwitterbot/tweet.txt','r') 
                 tweettext = filename.readlines() 
                 filename.close()
                 n = random.randint(0,1000)
                 for x in range(3): #Will only write first 5 lines
                   n = random.randint(0,1000)
                   twitter.update_status(status='@' + user + ' ' + tweettext[n],in_reply_to_status_id=data['id'])
                   time.sleep(5) # Sleep for 15 seconds 
                 message = '@' + user + ' CMD_RANDOMTWEET completed'
            twitter.update_status(status=message,in_reply_to_status_id=data['id'])
            #print("Tweeted: {}".format(message))

    def on_error(self, status_code, data):
        print(status_filtercode)
        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()

stream = MyStreamer(consumer_key, consumer_secret,
                    access_token, access_token_secret)
stream.statuses.filter(track='@SRPI7')   
