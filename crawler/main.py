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
    # targets = cm.get_config('target')['authors']
    # for author in targets:
    #     tmp = author.decode('utf-8')
    #     print u'开始下载%s的歌曲' % tmp
    #     Crawler().get_url_by_singer(author)
    #     DataProcedure().run()
    #     Baidu().searchBySinger(tmp)
    # 测试get_url_by_sname功能
    Crawler().get_url_by_sname('当爱已成往事')
    DataProcedure().run()
    Baidu().searchBySname(u'当爱已成往事')