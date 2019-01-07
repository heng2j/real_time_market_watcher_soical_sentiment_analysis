#!/bin/bash

python ./src/create_stream.py TweetsStream > create_stream_TweetsStream.py.out &
python ./src/create_stream.py StockTradeStream > create_stream_StockTradeStream.py.out &
