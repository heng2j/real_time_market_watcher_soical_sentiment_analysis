#!/usr/bin/env python3
# consumer_news.py
# ---------------
# Author: Zhongheng Li
# Start Date: 01-03-19
# Last Modified Date: 01-23-19


"""
This code save real time news data to AWS DynamoDB in every 15 mins

"""

# System modules
import json
import time
import uuid

import os
from os.path import dirname as up

import sys
import configparser


# projectPath = up(os.getcwd())
src_path = os.getcwd()
sys.path.append(src_path)



# 3rd party modules
import pyEX
import boto3
from botocore.exceptions import ClientError

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import sessionmaker

from dateutil import parser

# Internal Modules
from src.models import news
from src.data_tools import getSQL_DB_Engine


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

#
# def getSQL_DB_Engine( filePath=None):
#     """
#
#     :param filePath: DB configs ini file path
#     :return: SQLalchemy database engine
#     """
#
#     config = configparser.ConfigParser()
#     config.read(filePath)
#
#     DB_TYPE = config['DB_Configs']['DB_TYPE']
#     DB_DRIVER = config['DB_Configs']['DB_DRIVER']
#     DB_USER = config['DB_Configs']['DB_USER']
#     DB_PASS = config['DB_Configs']['DB_PASS']
#     DB_HOST = config['DB_Configs']['DB_HOST']
#     DB_PORT = config['DB_Configs']['DB_PORT']
#     DB_NAME = config['DB_Configs']['DB_NAME']
#     SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER,
#                                                           DB_PASS, DB_HOST, DB_PORT, DB_NAME)
#     engine = create_engine(
#         SQLALCHEMY_DATABASE_URI, echo=False)
#
#     return engine




if __name__ == '__main__':


    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StockNews')

    # Set up DB configs file path


    # DB_configs_ini_file_path = projectPath + "/DB/db_configs.ini"

    # print("DB_configs_ini_file_path: ", DB_configs_ini_file_path)

    DB_engine = getSQL_DB_Engine()

    while True:
        for symbol in symbolsList:

            latest_news_list = pyEX.news(symbol, count=100)

            for news_data in latest_news_list:
                news_item = {}

                news_item['datetime'] = '{0:%Y-%m-%d %H:%M:%S}'.format(parser.parse(news_data['datetime']))
                news_item['symbol'] = symbol
                news_item['headline'] = news_data['headline']
                news_item['related'] = news_data['related']
                news_item['source'] = news_data['source']
                news_item['summary'] = news_data['summary']


                stmt = pg_insert(news).values(news_item)
                # stmt = stmt.on_conflict_do_update(
                #     index_elements=[news.record_id],
                #     set_={'num_solved': stmt.excluded.num_solved,
                #           'num_accepts': stmt.excluded.num_accepts,
                #           'num_submissions': stmt.excluded.num_submissions,
                #           'accepted_percentage': stmt.excluded.accepted_percentage,
                #           'finished_contests': stmt.excluded.finished_contests, }
                # )
                try:
                    r = DB_engine.execute(stmt)
                except Exception as e:

                    if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                        raise

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

        time.sleep(10)


