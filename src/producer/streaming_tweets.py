from __future__ import absolute_import, print_function

import json
import time
from datetime import datetime
import configparser

import boto3
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener



config = configparser.ConfigParser()
config.read('../../configs.ini')

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = config['tweepy']['consumer_key']
consumer_secret = config['tweepy']['consumer_secret']

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = config['tweepy']['access_token']
access_token_secret = config['tweepy']['access_token_secret']


# tracking_list = ['#AAPL',
#                '#AMZN',
#                '#BA',
#                '#BAC',
#                '#BTI',
#                '#CAJ',
#                '#CAT',
#                '#CL',
#                '#COP',
#                '#CSCO',
#                '#CVX',
#                '#DVMT',
#                '#F',
#                '#FB'
#                '#GBIL',
#                '#GSK',
#                '#HD',
#                '#HMC',
#                '#BBL',
#                '#BOTZ',
#                '#JNJ',
#                '#AMJ',
#                '#KMB',
#                '#KOF',
#                '#MMM',
#                '#MSFT',
#                '#MUFG',
#                '#NAV',
#                '#NOC',
#                '#NVS',
#                '#PEP',
#                '#PFE',
#                '#PM',
#                '#RDS.A',
#                '#SAP',
#                '#SLB',
#                '#SNE',
#                '#SYMC',
#                '#TM',
#                 '#TSLA',
#                '#AOD',
#                '#TSM',
#                '#UL',
#                '#VLO',
#                '#WBA',
#                '#BDCL',
#                '#GJO',
#                '#XOM',
#                '#XRX']



tracking_list = ['#AAPL',
                 '#AMZN',
                 '#BAC',
                 '#BTI',
                 '#CAJ',
                 '#CSCO',
                 '#CVX',
                 '#DVMT',
                 '#FB'
                 '#GBIL',
                 '#GSK',
                 '#HMC',
                 '#BBL',
                 '#MSFT',
                 '#MUFG',
                 '#PFE',
                 '#RDS.A',
                 '#SAP',
                 '#SLB',
                 '#SNE',
                 '#SYMC',
                 '#TSLA',
                 '#AOD',
                 '#TSM',
                 '#UL',
                 '#VLO',
                 '#WBA',
                 '#BDCL',
                 '#GJO',
                 '#XOM',
                 '#XRX',
                 '#NBA']


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    def on_status(self, status):
        print(status.txt)

    def on_data(self, data):

        try:
            all_data = json.loads(data)
            tw_data = {}
            status_sent_entity = {}
            retweet_status_sent_entity = {}
            print("Collecting Tweet")

            if 'lang' in all_data and (all_data['lang'] == "en"):

                tw_data['searched_name'] = None

                tag_list = [dic.get('text').lower() for dic in all_data['entities']['hashtags']]

                for tag in tracking_list:

                    if tag.lower().replace('#', '') in tag_list:
                        tw_data['searched_name'] = tag.lower().replace('#', '')
                        break

                if tw_data['searched_name'] != None:

                    # print(all_data)

                    tw_data['timestamp'] = f"{datetime.now():%Y-%m-%d  %H:%M:%S}"
                    tw_data['status_id'] = str(all_data["id"])

                    tw_data['retweet_count'] = str(all_data['retweet_count'])
                    tw_data['favorite_count'] = str(all_data['favorite_count'])
                    tw_data['text'] = str(all_data['text'].encode('ascii', 'ignore').decode('ascii'))
                    tw_data['retweeted'] = all_data['retweeted']
                    tw_data['favorited'] = all_data['favorited']
                    tw_data['user_following'] = all_data['user']['following']
                    tw_data['user_friends_count'] = str(all_data['user']['friends_count'])
                    tw_data['user_location'] = str(all_data['user']['location'])
                    tw_data['user_favourites_count'] = str(all_data['user']['favourites_count'])
                    tw_data['user_name'] = all_data['user']['name']
                    tw_data['user_followers_count'] = str(all_data['user']['followers_count'])
                    tw_data['user_listed_count'] = str(all_data['user']['listed_count'])
                    tw_data['hashtags'] = str(all_data['entities']['hashtags'])

                    print('Putting this record to stream: ', tw_data)

                    try:
                        response = client.put_record(StreamName=stream_name, Data=json.dumps(tw_data),
                                                     PartitionKey=tw_data['searched_name'])


                    except Exception as e:
                        print("Failed Kinesis Put Record {}".format(str(e)))
                    pass

        except BaseException as e:
            print("failed on data ", str(e))
            time.sleep(5)

        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            return False


if __name__ == '__main__':
    client = boto3.client('kinesis')

    stream_name = 'TweetsStream'

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=tracking_list)
