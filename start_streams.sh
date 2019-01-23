#!/bin/bash

python3 ./src/create_stream.py TweetsStream > create_stream_TweetsStream.py.out &
python3 ./src/create_stream.py StockTradeStream > create_stream_StockTradeStream.py.out &
