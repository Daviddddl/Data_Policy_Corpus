import os
import sys
import random

from BaiduCrawler import crawler

rootdir = './ltp_res'
negative_urls = './nega_urls'


def get_nega_urls():
    files_list = os.listdir(rootdir)
    for line in files_list:
        filepath = os.path.join(rootdir, line)
        if os.path.isdir(filepath):
            print("dir:" + filepath)
        if os.path.isfile(filepath):
            if 'title' in filepath:
                # print("file:" + filepath)
                with open(filepath) as keywords:
                    keywords = keywords.read().strip().replace(" ", "")
                    print(keywords)
                    c = crawler(keywords)
                    c.set_timeout(int(random.random() * 10 / 3) + 1)
                    c.set_total_pages(1)
                    output_file = negative_urls + '/' + filepath[10:-4] + '_urls.txt'
                    print(output_file)
                    with open(output_file, 'w+') as output:
                        old = sys.stdout
                        sys.stdout = output
                        c.run()
                        sys.stdout = old


if __name__ == '__main__':
    get_nega_urls()
