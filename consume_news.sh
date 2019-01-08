#!/bin/bash#

#streaming_news
nohup python3 ./src/consumer/consumer_news.py > ./logs/consumer_news.py.out 2>&1 &
echo $! > consume_news_save_pid.txt
