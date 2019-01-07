#!/bin/bash

python3 ./src/delete_stream.py TweetsStream > delete_stream_TweetsStream.py.out &
python3 ./src/delete_stream.py StockTradeStream > delete_stream_StockTradeStream.py.out &
