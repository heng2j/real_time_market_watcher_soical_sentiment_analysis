#!/bin/bash

# streaming_tweets
echo 'streaming_tweets.py: ' > save_pid.txt
nohup python3 ./src/producer/streaming_tweets.py > ./logs/streaming_tweets.py.out 2>&1 &
echo $! >> save_pid.txt

nohup python3 ./src/consumer/consumer_stream.py --streamName TweetsStream --tableName TweetsStreamTweets > ./logs/consumer_stream_TweetsStream.out 2>&1 &
echo $! >> save_pid.txt

# streaming_stock
nohup python3 ./src/producer/streaming_stock.py > ./logs/streaming_stock.py.out 2>&1 &
echo $! >> save_pid.txt
nohup python3 ./src/consumer/consumer_stream.py --streamName StockTradeStream --tableName StockTradesProcessor > ./logs/consumer_stream_StockTradeStream.out  2>&1 &
echo $! >> save_pid.txt






