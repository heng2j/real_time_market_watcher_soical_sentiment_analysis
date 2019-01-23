#!/usr/bin/env python3
# delete_stream.py
# ---------------
# Author: Zhongheng Li
# Start Date: 01-03-19
# Last Modified Date: 01-06-19


"""
This code delete the stream on AWS Kinesis with given stream name

"""

# System modules
import sys
import os
import time

# 3rd party modules
import boto3
from botocore.exceptions import ClientError



# connect to the kinesis
# kinesis = boto.kinesis.connect_to_region(region)

def get_status(client,stream_name, shard_limit=1):

    response = None
    try:

        response = client.describe_stream(
                StreamName=stream_name
            )

    except ClientError as e:
        print(e)

    return response

def delete_stream(client,stream_name):
    return client.delete_stream(
            StreamName=stream_name,
            EnforceConsumerDeletion=True
        )



def main(search_name):
    stream_name = search_name[0]

    client = boto3.client('kinesis')

    try:
        delete_stream(client,stream_name)
        print('Deleting Kinesis stream... Please wait...')

        time.sleep(60)
    except ClientError as e:
        print(e)
        pass

    status = get_status(client,stream_name)
    if not status:
            print('stream {} is deleted'.format(stream_name))
    else:
        print('Stream Status: ', status)



if __name__ == '__main__':
    # Take the argument as the Stream Name to be deleted
    main(sys.argv[1:])