import datetime
import time
import json

from decimal import Decimal


from collections import defaultdict, Counter
from dateutil import parser
from operator import itemgetter


import json
import time
import pyEX
import pandas as pd
import boto3

from datetime import datetime
from pytz import timezone


from dateutil import parser


from collections import defaultdict, Counter
from dateutil import parser
from operator import itemgetter

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

            try:
                response = table.put_item(Item=news_item)
                print("PutItem succeeded:")
                print(json.dumps(response, indent=4, cls=DecimalEncoder))


            except Exception as e:
                print("Failed dynamodb Put Record {}".format(str(e)))
                pass


    # while True:
    #     print('Collecting Latest Stock Quotes')

    #     for symbol in symbolsList:

    #         stock_data = {}

    #         latest_price = pyEX.price(symbol)
    #         latest_quote = pyEX.quote(symbol)
    #         latest_time = latest_quote['latestTime']

    #         if latest_price != stocks_hist[symbol]['previous_price'] and latest_time != stocks_hist[symbol][
    #             'prevuius_time']:



    #             # Update stock_data
    #             stock_data['symbol'] = latest_quote['symbol']
    #             stock_data['companyName'] = latest_quote['companyName']
    #             stock_data['primaryExchange'] = latest_quote['primaryExchange']
    #             stock_data['sector'] = latest_quote['sector']
    #             stock_data['calculationPrice'] = latest_quote['calculationPrice']
    #             stock_data['open'] = latest_quote['open']
    #             stock_data['close'] = latest_quote['close']
    #             stock_data['high'] = latest_quote['high']
    #             stock_data['low'] = latest_quote['low']
    #             stock_data['latestPrice'] = latest_quote['latestPrice']
    #             stock_data['latestSource'] = latest_quote['latestSource']
    #             stock_data['latestTime'] =  datetime.now(timezone('US/Eastern')).strftime(fmt)
    #             stock_data['latestVolume'] = latest_quote['latestVolume']
    #             stock_data['previousClose'] = latest_quote['previousClose']
    #             stock_data['change'] = latest_quote['change']
    #             stock_data['changePercent'] = latest_quote['changePercent']
    #             stock_data['avgTotalVolume'] = latest_quote['avgTotalVolume']
    #             stock_data['marketCap'] = latest_quote['marketCap']
    #             stock_data['peRatio'] = latest_quote['peRatio']
    #             stock_data['week52High'] = latest_quote['week52High']
    #             stock_data['week52Low'] = latest_quote['week52Low']
    #             stock_data['ytdChange'] = latest_quote['ytdChange']

    #             if stocks_hist[symbol]['previous_price'] == 0:
    #               stock_data['movementPrice'] = latest_quote['latestPrice']
    #               stock_data['movementVolume'] = latest_quote['latestVolume']
    #             else:
    #               stock_data['movementPrice'] = stocks_hist[symbol]['previous_price'] - latest_quote['latestPrice']
    #               stock_data['movementVolume'] = latest_quote['latestVolume'] - stocks_hist[symbol]['previous_volume']

    #             # Update stocks_hist for comparison
    #             stocks_hist[symbol]['previous_price'] = latest_price
    #             stocks_hist[symbol]['previous_volume'] = latest_quote['latestVolume']
    #             stocks_hist[symbol]['prevuius_time'] = latest_time


    #             print('Putting this record to stream: ', stock_data)

    #             try:
    #                 response = client.put_record(StreamName=stream_name, Data=json.dumps(stock_data),
    #                                              PartitionKey=symbol)


    #             except Exception as e:
    #                 print("Failed Kinesis Put Record {}".format(str(e)))
    #             pass

    # time.sleep(5)

