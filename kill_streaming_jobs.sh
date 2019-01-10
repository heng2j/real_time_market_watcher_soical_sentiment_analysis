#!/bin/bash

$stock_sentiment_analysis_PATH

filename="save_pid.txt"

#While loop to read each stored PIDs line by line
while read -r line
do
    readLine=$line

    if [[ "$readLine" =~ ^[0-9]+$ ]]

        then
                kill -9 "$readLine"

    fi
done < "$filename"