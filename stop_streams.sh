#!/bin/bash

python3 ./src/delete_stream.py TweetsStream > ./logs/delete_stream_TweetsStream.py.out &
python3 ./src/delete_stream.py StockTradeStream > ./logs/delete_stream_StockTradeStream.py.out &
