#!/bin/bash#

streaming_news
nohup python3 ./src/consumer/consumer_news.py > ./logs/consumer_news.py.out 2>&1 &
echo $! > save_pid.txt
