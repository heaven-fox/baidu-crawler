# coding: utf-8
from crawler.db.dbmanager import DBManager
from crawler.conf.cm import ConfigManager
import crawler.task.download as download


class Baidu():
    def __init__(self):
        self.cm = ConfigManager()
        self.db = DBManager()

    def __del__(self):
        self.db.close()

    # 根据歌曲名称查询
    # 优先搜索数据库, 若找到, 直接返回该数据
    # 提示用户是否仍要继续下载
    # 否则, 联网搜索, 并将新数据存入数据库
    def searchBySinger(self, author):
        table = '%sresult' % self.cm.get_config('table')[0]['song']['prefix']
        sql_search = ('SELECT sname, durl FROM %s ' % table) + 'WHERE author = \'%s\'' % author
        data = self.db.query(sql_search)
        size = len(data)
        print('数据库目前收录%d首' % size)
        print '分别有:'
        for l in data:
            print(l[0])
        print('是否开始下载?(y/n)')
        choice = raw_input()
        if choice == 'y':
            base_dir = self.cm.get_config('dir')['path']
            download.download_all(data, base_dir, author, size)
        else:
            print '已取消下载'

    def searchBySname(self, sname, singer=None):
        """
        提供对外调用的接口, 接受歌曲名作为参数
        :param sname: 歌曲名
        :param singer: 歌手名(选项)
        :return:
        """
        table = '%sresult' % self.cm.get_config('table')[0]['song']['prefix']
        sql_search = ('SELECT author, durl FROM %s ' % table) + 'WHERE sname = \'%s\'' % sname
        data = self.db.query(sql_search)
        size = len(data)
        print('数据库目前收录%d首' % size)
        print '分别有:'
        for l in data:
            print(l[0])
        print('是否开始下载?(y/n)')
        choice = raw_input()
        if choice == 'y':
            base_dir = self.cm.get_config('dir')['path']
            download.download_all(data, base_dir, sname, size)
        else:
            print '已取消下载'