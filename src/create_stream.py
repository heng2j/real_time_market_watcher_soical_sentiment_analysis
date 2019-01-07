#!/usr/bin/env python3
# create_stream.py
# ---------------
# Author: Zhongheng Li
# Start Date: 01-03-19
# Last Modified Date: 01-06-19


"""
This code create the stream to AWS Kinesis


Sample Usage:

python create_stream.py TweetsStream

"""

# System modules
import sys
import time

# 3rd party modules
import boto3
from botocore.exceptions import ClientError


def get_status(client,stream_name, shard_limit=1):

    response = client.describe_stream(
            StreamName=stream_name,
            Limit=shard_limit
        )

    return response.get('StreamDescription').get('StreamStatus')


def create_stream(client,stream_name):
    return client.create_stream(
                    StreamName=stream_name,
                    ShardCount=1
                )


def main(search_name):
    stream_name = search_name[0]

    client = boto3.client('kinesis')

    try:
        create_stream(client,stream_name)
        print('Creating Kinesis stream... Please wait...')

        time.sleep(60)
    except ClientError as e:
        print(e)
        pass


    # wait for the stream to become active
    while get_status(client,stream_name) != 'ACTIVE':
        time.sleep(1)
    print('stream {} is active'.format(stream_name))
    print( "\n ==== KINESES ONLINE ====")




if __name__ == '__main__':

    # Take the argument as the Stream Name to be created
    main(sys.argv[1:])