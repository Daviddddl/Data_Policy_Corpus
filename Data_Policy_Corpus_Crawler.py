#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import json
import re
import sys

import requests as req
from bs4 import BeautifulSoup

DBUG = 0

reBODY = re.compile(r'<body.*?>([\s\S]*?)<\/body>', re.I)
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
reTAG = r'<[\s\S]*?>|[ \t\r\f\v]'
reIMG = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')


class Extractor():
    def __init__(self, url="", blockSize=3, timeout=5, image=False):
        self.url = url
        self.blockSize = blockSize
        self.timeout = timeout
        self.saveImage = image
        self.rawPage = ""
        self.ctexts = []
        self.cblocks = []

    # 获取网页源码
    def getRawPage(self, encoding):
        try:
            resp = req.get(self.url, timeout=self.timeout)
        except Exception as e:
            raise e

        if DBUG: print(resp.encoding)

        resp.encoding = encoding

        return resp.status_code, resp.text

    def processTags(self):
        self.body = re.sub(reCOMM, "", self.body)
        self.body = re.sub(reTRIM.format("script"), "", re.sub(reTRIM.format("style"), "", self.body))
        self.body = re.sub(reTAG, "", self.body)

    def processBlocks(self):
        self.ctexts = self.body.split("\n")
        self.textLens = [len(text) for text in self.ctexts]

        self.cblocks = [0] * (len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x, y: x + y, self.textLens[i: lines - 1 - self.blockSize + i], self.cblocks))

        maxTextLen = max(self.cblocks)

        if DBUG: print(maxTextLen)

        self.start = self.end = self.cblocks.index(maxTextLen)
        while self.start > 0 and self.cblocks[self.start] > min(self.textLens):
            self.start -= 1
        while self.end < lines - self.blockSize and self.cblocks[self.end] > min(self.textLens):
            self.end += 1

        return "".join(self.ctexts[self.start:self.end])

    def processImages(self):
        self.body = reIMG.sub(r'{{\1}}', self.body)

    def getContext(self, encoding):
        code, self.rawPage = self.getRawPage(encoding)
        self.body = re.findall(reBODY, self.rawPage)[0]

        if DBUG: print(code, self.rawPage)

        if self.saveImage:
            self.processImages()
        self.processTags()
        return re.sub("&nbsp;", '', self.processBlocks())

    def getTitle(self):
        code, self.rawPage = self.getRawPage("gb2312")
        self.body = re.findall(reBODY, self.rawPage)[0]

        if DBUG: print(code, self.rawPage)

        soup = BeautifulSoup(self.body, 'html5lib')
        i = 1
        details = ''
        result_list = []
        for idx, tr in enumerate(soup.find_all('tr')):
            i += 1
            if i == 8:
                tds = tr.find_all('td')
                result_list.append({'title': str(tds[0].contents[0])[3:-4]})
            if i == 9 or i == 10:
                tds = tr.find_all('td')
                details += str(tds[0].contents[0])[1:] + ' | '
            if i == 11:
                result_list.append({'details': details[:-5]})
                break
        return result_list

    def getAll(self):
        code, self.rawPage = self.getRawPage("gb2312")
        self.body = re.findall(reBODY, self.rawPage)[0]
        if '传入参数错误，请联系管理员！' in self.body:
            return {'flag': False}
        else:
            context = re.sub("\u3000", '', ext.getContext("gb2312"))
            titleAnddetails = self.getTitle()
            title = titleAnddetails[0]['title']
            detail = titleAnddetails[1]['details']
            return {'flag': True, 'title': title, 'detail': detail, 'context': context}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='数据政策语料库爬虫工具')
    parser.add_argument('-u', '--url', help="Type: Str. Input the web's url")
    parser.add_argument('-a', '--all', type=bool, default=False,
                        help="Type: bool. Default: False. Get the web title, details and context.")
    parser.add_argument('-t', '--title', type=bool, default=False, help="Type: bool. Default: False. Get the web title")
    parser.add_argument('-d', '--details', type=bool, default=False,
                        help="Type: bool. Default: False. Get the web details")
    parser.add_argument('-c', '--context', type=bool, default=False,
                        help="Type: bool. Default: False. Get the web context")
    parser.add_argument('-o', '--output', help="Type: Str. Output file path")
    parser.add_argument('-s', '--simple', help="Type: Str. Simple version. And -s is the encoding "
                                               "which u need to specify.")

    ARGS = parser.parse_args()
    print(ARGS)
    if ARGS.url is not None:
        ext = Extractor(url=ARGS.url, blockSize=5, image=False)

        if ARGS.simple is not None:
            res = ext.getContext(ARGS.simple)
            print(res)
            if ARGS.output is not None:
                with open(ARGS.output, 'w+') as f:
                    f.write(res)
            sys.exit(0)

        if ext.getAll()['flag'] is True:
            if ARGS.all is True:
                # print(ext.getAll())
                if ARGS.output is not None:
                    with open(ARGS.output, 'w+') as f:
                        f.write(json.dumps(ext.getAll(), ensure_ascii=False))
            if ARGS.title is True:
                # print(ext.getAll()['title'])
                if ARGS.output is not None:
                    with open(ARGS.output, 'w+') as f:
                        f.write(json.dumps(ext.getAll()['title'], ensure_ascii=False))
            if ARGS.details is True:
                # print(ext.getAll()['detail'])
                if ARGS.output is not None:
                    with open(ARGS.output, 'w+') as f:
                        f.write(json.dumps(ext.getAll()['detail'], ensure_ascii=False))
            if ARGS.context is True:
                # print(ext.getAll()['context'])
                if ARGS.output is not None:
                    with open(ARGS.output, 'w+') as f:
                        f.write(json.dumps(ext.getAll()['context'], ensure_ascii=False))
        else:
            # print('传入的URL有误，网站无此链接！')
            if ARGS.output is not None:
                with open(ARGS.output, 'w+') as f:
                    f.write(json.dumps({'title': '传入的URL有误，网站无此链接！'}, ensure_ascii=False))
    else:
        parser.print_help()
        sys.exit(0)
