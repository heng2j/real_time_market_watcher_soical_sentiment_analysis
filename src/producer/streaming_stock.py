#!/usr/bin/env python3
# streaming_stock.py
# ---------------
# Author: Zhongheng Li
# Start Date: 01-03-19
# Last Modified Date: 01-06-19


"""
This code stream real time stock data to AWS Kinesis

"""

# System modules
from __future__ import absolute_import, print_function
from argparse import ArgumentParser

# 3rd party modules
import json
import time
import pyEX
import boto3

from datetime import datetime
from pytz import timezone



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

def main(client,stream_name):


    fmt = "%Y-%m-%d %H:%M:%S"

    stocks_hist = {}

    for symbol in symbolsList:
        stocks_hist[symbol] = {}
        stocks_hist[symbol]['previous_price'] = 0
        stocks_hist[symbol]['previous_volume'] = 0
        stocks_hist[symbol]['previous_time'] = ''

    while True:
        print('Collecting Latest Stock Quotes')

        for symbol in symbolsList:

            stock_data = {}

            latest_price = pyEX.price(symbol)
            latest_quote = pyEX.quote(symbol)
            latest_time = latest_quote['latestTime']

            if latest_price != stocks_hist[symbol]['previous_price'] and latest_time != stocks_hist[symbol][
                'previous_time']:

                # Update stock_data
                stock_data['symbol'] = latest_quote['symbol']
                stock_data['companyName'] = latest_quote['companyName']
                stock_data['primaryExchange'] = latest_quote['primaryExchange']
                stock_data['sector'] = latest_quote['sector']
                # stock_data['calculationPrice'] = latest_quote['calculationPrice']
                stock_data['open'] = latest_quote['open']
                stock_data['close'] = latest_quote['close']
                stock_data['high'] = latest_quote['high']
                stock_data['low'] = latest_quote['low']
                stock_data['latestPrice'] = latest_quote['latestPrice']
                stock_data['latestSource'] = latest_quote['latestSource']

                stock_data['latestTime'] = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(latest_quote['latestUpdate']/1000)) # datetime.now(timezone('US/Eastern')).strftime(fmt)
                stock_data['latestVolume'] = latest_quote['latestVolume']
                stock_data['previousClose'] = latest_quote['previousClose']
                stock_data['change'] = latest_quote['change']
                stock_data['changePercent'] = latest_quote['changePercent']
                stock_data['avgTotalVolume'] = latest_quote['avgTotalVolume']
                stock_data['marketCap'] = latest_quote['marketCap']
                stock_data['peRatio'] = latest_quote['peRatio']
                stock_data['week52High'] = latest_quote['week52High']
                stock_data['week52Low'] = latest_quote['week52Low']
                stock_data['ytdChange'] = latest_quote['ytdChange']

                if stocks_hist[symbol]['previous_price'] == 0:
                    stock_data['movementPrice'] = 0
                    stock_data['movementVolume'] = 0
                else:
                    stock_data['movementPrice'] = (
                                                  latest_quote['latestPrice'] - stocks_hist[symbol]['previous_price']) / \
                                                  stocks_hist[symbol]['previous_price']
                    stock_data['movementVolume'] = (latest_quote['latestVolume'] - stocks_hist[symbol][
                        'previous_volume']) / stocks_hist[symbol]['previous_volume']

                # Update stocks_hist for comparison
                stocks_hist[symbol]['previous_price'] = latest_price
                stocks_hist[symbol]['previous_volume'] = latest_quote['latestVolume']
                stocks_hist[symbol]['previous_time'] = latest_time

                print('Putting this record to stream: ', stock_data)

                try:
                    response = client.put_record(StreamName=stream_name, Data=json.dumps(stock_data),
                                                 PartitionKey=symbol)


                except Exception as e:
                    print("Failed Kinesis Put Record {}".format(str(e)))
                pass

        time.sleep(5)


if __name__ == '__main__':

    # # Set up argument parser
    # parser = ArgumentParser()
    # parser.add_argument("-sn", "--streamName", help="Input Stream Name", required=True)
    # args = parser.parse_args()
    #
    # # Assign input, output files and number of lines variables from command line arguments
    # stream_name = args.streamName


    client = boto3.client('kinesis')

    stream_name = 'StockTradeStream'

    main(client, stream_name)

