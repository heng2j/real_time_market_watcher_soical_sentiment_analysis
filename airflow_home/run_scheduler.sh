#!/bin/bash

echo 'airflow scheduler PID: ' > save_pid.txt
nohup airflow scheduler > ./logs/streaming_tweets.py.out 2>&1 &
echo $! >> save_pid.txt


