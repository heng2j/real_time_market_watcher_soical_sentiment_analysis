#!/usr/bin/env python3
# consumer_news.py
# ---------------
# Author: Zhongheng Li
# Start Date: 01-03-19
# Last Modified Date: 01-06-19


"""
This code save real time news data to AWS DynamoDB in every 15 mins

"""

# System modules
import json
import time

import pyEX
import boto3
from botocore.exceptions import ClientError

from dateutil import parser


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


symbolsList = ['AAPL',
               'AMZN',
               'BA',
               'BAC',
               'BTI',
               'CAJ',
               'CAT',
               'CL',
               'COP',
               'CSCO',
               'CVX',
               'DVMT',
               'F',
               'FB',
               'GBIL',
               'GSK',
               'HD',
               'HMC',
               'BBL',
               'BOTZ',
               'JNJ',
               'AMJ',
               'KMB',
               'KOF',
               'MMM',
               'MSFT',
               'MUFG',
               'NAV',
               'NOC',
               'NVS',
               'PEP',
               'PFE',
               'PM',
               'RDS.A',
               'SAP',
               'SLB',
               'SNE',
               'SYMC',
               'TM',
               'TSLA',
               'AOD',
               'TSM',
               'UL',
               'VLO',
               'WBA',
               'BDCL',
               'GJO',
               'XOM',
               'XRX']




if __name__ == '__main__':


    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StockNews')

    while True:

        for symbol in symbolsList:

            latest_news_list = pyEX.news(symbol, count=10)

            for news_data in latest_news_list:
                news_item = {}

                news_item['datetime'] = '{0:%Y-%m-%d %H:%M:%S}'.format(parser.parse(news_data['datetime']))
                news_item['symbol'] = symbol
                news_item['headline'] = news_data['headline']
                news_item['related'] = news_data['related']
                news_item['source'] = news_data['source']
                news_item['summary'] = news_data['summary']


                try:
                    response = table.put_item(
                        Item=news_item,
                        ConditionExpression='attribute_not_exists(symbol) AND attribute_not_exists(headline)'
                    )
                    print("PutItem succeeded:")
                    print(json.dumps(response, indent=4, cls=DecimalEncoder))

                except ClientError as e:
                    # Ignore the ConditionalCheckFailedException, bubble up
                    # other exceptions.
                    if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                        raise

        time.sleep(900)


