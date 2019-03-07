```shell
pip install -r requirements.txt
```
# Data_Policy_Corpus
爬取 http://210.46.97.225/gov_corpus/corpus_look1553.html 这些链接
# 示例用法
python Data_Policy_Corpus_Crawler.py -u http://210.46.97.225/gov_corpus/corpus_look1553.html -a 1
# 也可以重定向到指定文件
python Data_Policy_Corpus_Crawler.py -u http://210.46.97.225/gov_corpus/corpus_look1553.html -a 1 > test.txt
# Usage
python Data_Policy_Corpus_Crawler.py

# LTP 分词使用
python LTPez.py -c "众所周知，我有一个伟大的梦想" -t doc

具体有哪些type，请参考 python LTPez.py -c "众所周知，我有一个伟大的梦想" -p 1