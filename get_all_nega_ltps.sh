#!/usr/bin/env bash

for file in `ls ./nega_webs`
do
    echo $file
    sed -n "2p" ./nega_webs/$file > ./tmp.txt
    python LTPez.py -f ./tmp.txt -t words_cont -o ./ltp_res_nega/$file -p 1
done
