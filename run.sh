#!/bin/bash

# streaming_tweets
nohup python ./src/producer/streaming_tweets.py > ./logs/streaming_tweets.py.out &
nohup python ./src/consumer/consumer_stream.py --streamName TweetsStream --tableName TweetsStreamTweets > ./logs/consumer_stream_TweetsStream.out &


# streaming_stock
nohup python ./src/producer/streaming_stock.py > ./logs/streaming_stock.py.out &
nohup python ./src/consumer/consumer_stream.py --streamName StockTradeStream --tableName StockTradesProcessor > ./logs/consumer_stream_StockTradeStream.out &







