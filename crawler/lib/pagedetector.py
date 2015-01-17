# coding: utf-8

import pycurl
from StringIO import StringIO
from bs4 import BeautifulSoup
import re
page_pattern = re.compile('page-navigator-hook*')
digit_pattern = re.compile(r'\D')


class PageDetector():
    def __init__(self):
        # 完成初始化工作
        pass

    # 负责收集歌手收录的歌曲数量
    @classmethod
    def detect(cls, author):
        buffers = StringIO()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, 'http://music.baidu.com/search/song?key=%s&s=1' % author)
        curl.setopt(curl.USERAGENT, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0)"
                                    " Gecko/20100101 Firefox/34.0")
        curl.setopt(curl.WRITEDATA, buffers)
        curl.perform()
        curl.close()
        body = buffers.getvalue()
        soup = BeautifulSoup(body)
        # 返回一个list
        content = soup.find('div', {'class': 'search-song-list song-list song-list-hook'}).findAll\
            ('li', {'class': 'bb-dotimg clearfix song-item-hook  '})
        page_ori = soup.find('div', {'class': page_pattern})['class']
        soup.decompose()
        # 获取总歌曲数, 每页显示歌曲数
        s_total = int(digit_pattern.sub('', page_ori[4]))
        s_size = int(digit_pattern.sub('', page_ori[5]))

        return s_total, s_size