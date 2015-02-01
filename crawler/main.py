# coding: utf-8

import build.setup as setup
from api.baidu import Baidu
from task.dataprocessor import DataProcedure
from lib.songcrawler import Crawler
import build.clean as clean
from conf.cm import ConfigManager
cm = ConfigManager()

if __name__ == '__main__':
    setup.setup_env()
    clean.cleanup()
    targets = cm.get_config('target')['authors']
    for author in targets:
        tmp = author.decode('utf-8')
        print u'开始下载%s的歌曲' % tmp
        Crawler().run(author)
        DataProcedure().run()
        Baidu().searchBySinger(tmp)
