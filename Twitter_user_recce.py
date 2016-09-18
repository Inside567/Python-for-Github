import requests 
import json
import time
import sys

from requests_oauthlib import OAuth1

target = (sys.argv[1])

# begin timer

t1 = time.clock()

#define time variable

localtime = time.asctime( time.localtime(time.time()) )

#authentication pieces

client_key = ""
client_secret = ""
token = ""
token_secret = ""

#base for all Twitter calls

base_twitter_url = "https://api.twitter.com/1.1"

#setup auth

oauth = OAuth1(client_key,client_secret,token,token_secret)

# Download Tweets from a user profile without RTs

def download_tweets(screen_name,number_of_tweets):
    
    api_url = "%s/statuses/user_timeline.json?" % base_twitter_url
    api_url += "screen_name=%s&" % screen_name
    api_url += "count=%d&" % number_of_tweets
    api_url += "include_rts=false" # code for excluding retweets
    response = requests.get(api_url,auth=oauth)
    print "\n[*]",api_url
    print "[*]",response
    if response.status_code == 200:
        tweets = json.loads(response.content)
        return tweets
    else:
        print "Account does not exist, or there was another error" # terminate the script if the response is anything other than a 200
        quit()
    return None    

# Download Tweets from a user profile including RTs

def download_all_tweets(screen_name,number_of_tweets):
    
    api_url = "%s/statuses/user_timeline.json?" % base_twitter_url
    api_url += "screen_name=%s&" % screen_name
    api_url += "count=%d" % number_of_tweets
    response = requests.get(api_url,auth=oauth)
    print "[*]",api_url
    print "[*]",response
    if response.status_code == 200:
        tweets = json.loads(response.content)
        return tweets
    return None    

# grab last 200 tweets (no RTs)

def download_200():
    dlt = download_tweets(target,200)
    for item in dlt:
        rtc = item['retweet_count'] # add the values for number of times that tweet has been re-tweeted
        tc = item['text'].encode('cp850', errors='replace')
        rt_list.append(rtc) # add the re-tweet value to the rt_list
        
# grab last 200 tweets (including RTs)

rt_list1 = [] # create an empty list for storing rt values, this is so we can count it later and get the value

def download_200_rt():
    dlt1 = download_all_tweets(target,200)
    for item in dlt1:
        rt_list1.append(item)
    
# logic to work out average retweets

rt_list = [] # make a list for adding all the tweets to
download_200() # run function
download_200_rt() # run function
rt_list.sort() # sort the rt_list into numerical order 

rtc_lowest = rt_list[0] # pull the lowest value from the rt_list 
rtc_highest = rt_list[-1] # pull the highest value from rt_list
rtc_count = len(rt_list) # count the rt_list
alltweet_count = len(rt_list1) #
rtc_avg = sum(rt_list) / float(len(rt_list))

rt_perc = (float(alltweet_count) - float(rtc_count)) / float(alltweet_count) * 100
ot_perc = 100.00 - float(rt_perc)
print "[*] target =", target
print "[*]", rtc_count, "/", alltweet_count, "(%f" % ot_perc, "%) original tweets"
print "[*]", alltweet_count - rtc_count, "/", alltweet_count, "(%f" % rt_perc, "%) are reweets"
print "[*]",round(rtc_avg,2), "average number of retweets"
print "[*]", rtc_lowest, "lowest retweet value"
print "[*]", rtc_highest, "highest retweet value"

print "///////////////// Whole process took",time.clock() - t1, "seconds /////////////////"   
 
