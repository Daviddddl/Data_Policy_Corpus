#!/usr/bin/env bash

for ((i=1; i<=1549; i++))
do
    echo $i
    python Data_Policy_Corpus_Crawler.py -u http://210.46.97.225/gov_corpus/corpus_look$i.html -a True -o ./raw_data/$i.json
    sleep $((1 + RANDOM % 3))
done
