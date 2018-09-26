#!/usr/bin/env bash

for ((i=1556; i<=1549; i++))
do
    echo $i
    python Data_Policy_Corpus_Crawler.py -u http://210.46.97.225/gov_corpus/corpus_look$i.html -a 1 > ./raw_data/$i.txt
	sleep $((1 + RANDOM % 3))
done