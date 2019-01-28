#!/usr/bin/env python3
# consumer_stream.py
# ---------------
# Author: Zhongheng Li
# Start Date: 01-03-19
# Last Modified Date: 01-06-19


"""
This code

"""

# System modules
import time
from decimal import Decimal
import json
from argparse import ArgumentParser
import sys
import os
from os.path import dirname as up

# projectPath = up(os.getcwd())
src_path = os.getcwd()
sys.path.append(src_path)

# print(src_path)

# 3rd party modules
import boto3
from botocore.exceptions import ClientError
from sqlalchemy.dialects.postgresql import insert as pg_insert


# Internal Modules
from src.models import tweet, trade
from src.data_tools import getSQL_DB_Engine


class KinesisConsumer:
    """Generic Consumer for Amazon Kinesis Streams"""
    def __init__(self, stream_name,table_name, shard_id, iterator_type,
                 worker_time=30, sleep_interval=0.5):


        self.stream_name = stream_name
        self.table_name = table_name
        self.shard_id = str(shard_id)
        self.iterator_type = iterator_type
        self.worker_time = worker_time
        self.sleep_interval = sleep_interval
        
    def process_records(self, records):
        """the main logic of the Consumer that needs to be implemented"""
        raise NotImplementedError
    
    @staticmethod
    def iter_records(records):
        for record in records:
            part_key = record['PartitionKey']
            data = record['Data']
            yield part_key, data
    
    def run(self):
        """poll stream for new records and pass them to process_records method"""
        response = kinesis.get_shard_iterator(StreamName=self.stream_name,ShardId=self.shard_id, ShardIteratorType=self.iterator_type)
        
        next_iterator = response['ShardIterator']

        while True:
            try:
                response = kinesis.get_records(ShardIterator = next_iterator, Limit=100)
        
                records = response['Records']
            
                if records:
                    self.process_records(records)
            
                next_iterator = response['NextShardIterator']
                time.sleep(self.sleep_interval)
            except ClientError as ptee:
                time.sleep(1)



# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class saveStreamDataToDynamoDB(KinesisConsumer):
    """Consumers that echos received data to standard output"""

    def process_records(self, records):
        """print the partion key and data of each incoming record"""
        for part_key, data in self.iter_records(records):
            all_data = json.loads(data)

            all_data = json.loads(json.dumps(all_data), parse_float=Decimal)


            if stream_name == 'TweetsStream':
                stmt = pg_insert(tweet).values(all_data)
            elif  stream_name == 'StockTradeStream':

                all_data_lower = {k.casefold(): v for k, v in all_data.items()}

                print(all_data_lower)
                stmt = pg_insert(trade).values(all_data_lower)



            try:
                r = DB_engine.execute(stmt)
            except Exception as e:

                if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                    raise




            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(self.table_name)

            try:
                response = table.put_item(Item=all_data)
                print("PutItem succeeded:")
                print(json.dumps(response, indent=4, cls=DecimalEncoder))


            except Exception as e:
                print("Failed dynamodb Put Record {}".format(str(e)))
                pass






if __name__ == '__main__':
    # Set up argument parser
    parser = ArgumentParser()
    parser.add_argument("-sn", "--streamName", help="Input Stream Name", required=True)
    parser.add_argument("-tn", "--tableName", help="Destination DataBase Table Name", required=True)

    args = parser.parse_args()

    # python consumer_stream.py --streamName TweetsStream --tableName TweetsStreamTweets

    # Assign input, output files and number of lines variables from command line arguments
    stream_name = args.streamName
    table_name = args.tableName


    # Set up DB_engine
    DB_engine = getSQL_DB_Engine()


    kinesis = boto3.client('kinesis')
    # stream_name = 'StockTradeStream'
    # table_name = 'StockTradesProcessor'
    # stream_name = 'TweetsStream'
    # table_name = 'TweetsStreamTweets'


    shard_id = 'shardId-000000000000'
    iterator_type =  'LATEST'
    worker = saveStreamDataToDynamoDB(stream_name,table_name, shard_id, iterator_type, worker_time=6000)
    worker.run()

