#!/usr/bin/env bash

for ((i=4; i<=1921; i++))
do
    echo "python LTPez.py -f ./tmp.txt -t words_cont -o ./ltp_res/$i.txt"
    sed -n "2p" ./raw_data/$i.txt > ./tmp.txt
    python LTPez.py -f ./tmp.txt -t words_cont -o ./ltp_res/$i.txt
done