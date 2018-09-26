#!/usr/bin/env bash

for file in `ls ./nega_urls`
do
#    echo "./nega_urls/"$file
    i=0
    cat ./nega_urls/$file | while read line
    do
        echo ${line}
        ((i=$i+1))
#        echo $i
        python Data_Policy_Corpus_Crawler.py -u ${line} -s 1 > ./nega_webs/$file$i.txt
    done
done