# coding: utf-8

import pycurl
from StringIO import StringIO
import bs4
from bs4 import BeautifulSoup
from crawler.tool.dataserialization import DataSerialization
from crawler.conf.cm import ConfigManager
from pagedetector import PageDetector
import redis
import re
pattern = re.compile(r'\\')

# 伪装客户端
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0"


class Crawler():
    def __init__(self):
        self.serialization = DataSerialization()
        self.cm = ConfigManager()

    def run(self, author):
        """
        接受author参数, 获取其在百度音乐上收录的所有歌曲, 按照['sid', 'author', 'sname', 'download_counts']元组形式
        压入redis数据库, 由后台的task程序处理
        :param author: 歌手名
        :return:
        """
        s_total, s_size = PageDetector.detect(author)
        queue_data = self.cm.get_config('taskqueue')['data']
        r = redis.Redis(
            host=self.cm.get_config('redis')['host'],
            port=self.cm.get_config('redis')['port']
        )
        if not r:
            print 'Redis服务未启动'
        else:
            print 'Redis服务正常'
        pages = (s_total + s_size - 1)/s_size
        list1 = []
        sids = '{'
        # 维护一个计数器, 到达5时, 触发url探测
        # 之后, 清零, 并重置sids和list1
        counts = 0
        for i in xrange(pages):
            start = i*s_size
            print '第%d页' % (i+1)
            if counts == 5:
                sids += '}'
                # step 3: 获取歌曲真实下载地址
                download_url = 'http://play.baidu.com/data/music/songlink?songIds=%s' % sids
                curl = pycurl.Curl()
                buffers = StringIO()
                curl.setopt(curl.URL, download_url)
                curl.setopt(curl.USERAGENT, user_agent)
                curl.setopt(curl.WRITEDATA, buffers)
                curl.perform()
                curl.close()
                body = buffers.getvalue()
                soup = BeautifulSoup(body)
                song_lists = self.serialization.json_to_data(soup.text)['data']['songList']
                soup.decompose()
                counter = 0
                # step 4: 封装歌曲信息
                for item in list1:
                    links = song_lists[counter]['songLink']
                    # print links
                    if not links:
                        url = 'zzz'
                    else:
                        url = pattern.sub('', links)
                    item.append(url)
                    # print item
                    counter += 1
                # step 5: 压入redis
                print '开始提交数据'
                r.lpush(queue_data, list1)
                print '数据压入redis完毕'
                list1 = []
                sids = '{'
                counts = 0

            # step 1: 搜索歌手, 获取歌曲id
            buffers = StringIO()
            curl = pycurl.Curl()
            # 伪造来源
            refer_url = 'http://music.baidu.com/search?key=%s' % author
            search_url = 'http://music.baidu.com/search/song?s=1&key=%s&start=%d&size=%d' % (author, start, s_size)
            # print tmp_url
            curl.setopt(curl.URL, search_url)
            curl.setopt(curl.USERAGENT, user_agent)
            curl.setopt(pycurl.REFERER, refer_url)
            curl.setopt(curl.WRITEDATA, buffers)
            curl.perform()
            curl.close()
            body = buffers.getvalue()
            soup = BeautifulSoup(body)
            # 返回一个list
            content = soup.find('div', {'class': 'search-song-list song-list song-list-hook'}).findAll\
                ('li', {'class': 'bb-dotimg clearfix song-item-hook  '})
            soup.decompose()
            # step 2: 获取歌曲基本信息
            counts += 1
            if not content:
                continue
            for tag in content:
                songitem = self.serialization.json_to_data((tag['data-songitem']))['songItem']
                sid = songitem['sid']
                # print sid
                if not isinstance(sid, int):
                    continue
                sids += str(sid) + ','
                sname = tag.find('div', {'class': 'song-item'}).find('span', {'class': 'song-title'}).find('a').text
                list1.append([sid, author, sname, 1])

    def get_url_by_sname(self, sname, author=None):
        """
        接受歌曲名作为参数, 搜索其对应的列表, 这里做个处理, 只是抽取列表第1页的数据, 后面的数据参考性不是很大
        :param sname: 歌曲名
        :param author: 歌手名, 仅当用户定点查询歌手的某首歌时, 才开启该选项; 默认None
        :return:
        """
        search_url = 'http://music.baidu.com/search?key=%s' % sname
        refer_url = 'http://music.baidu.com/'
        buffers = StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, search_url)
        curl.setopt(pycurl.REFERER, refer_url)
        curl.setopt(pycurl.USERAGENT, user_agent)
        curl.setopt(pycurl.WRITEDATA, buffers)
        curl.perform()
        curl.close()

        body = buffers.getvalue()
        soup = BeautifulSoup(body)

        content = soup.find('div', {'id': 'result_container'}).find('ul')
        soup.decompose()
        song_list = []
        sids = '{'
        for tag in content:
            # 删除注释行
            if isinstance(tag, bs4.element.Comment):
                continue
            item = self.serialization.json_to_data(tag.get('data-songitem'))['songItem']
            sid = item['sid']
            author = item['author']
            sids += str(sid) + ','
            song_list.append([sid, author, sname, 1])
        sids += '}'
        urls = self.get_url_by_sid(sids)
        counter = 0
        for item in song_list:
            item.append(urls[counter])
            counter += 1
        print(song_list)
        # @ TODO 歌曲链接处理

    def get_url_by_sid(self, sids):
        """
        接受歌曲id构成的字符串
        :param sids: 歌曲id串
        :return: 歌曲真实下载url
        """
        search_url = 'http://play.baidu.com/data/music/songlink?songIds=%s' % sids
        buffers = StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, search_url)
        curl.setopt(pycurl.USERAGENT, user_agent)
        curl.setopt(pycurl.WRITEDATA, buffers)
        curl.perform()
        curl.close()

        body = buffers.getvalue()
        soup = BeautifulSoup(body)

        song_lists = self.serialization.json_to_data(soup.text)['data']['songList']
        soup.decompose()
        urls = []
        for l in song_lists:
            link = l['songLink']
            if not link:
                url = 'zzz'
            else:
                url = pattern.sub('', link)
            urls.append(url)
        return urls