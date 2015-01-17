# coding: utf-8
import redis
from crawler.db.dbmanager import DBManager
from crawler.conf.cm import ConfigManager


class DataProcedure():
    def __init__(self):
        self.cm = ConfigManager()
        self.db = DBManager()

    def __del__(self):
        self.db.close()

    def run(self):
        sql = self.get_sql()
        queue_data = self.cm.get_config('taskqueue')['data']
        queue_back = self.cm.get_config('taskqueue')['backup']
        r = redis.Redis(
            host=self.cm.get_config('redis')['host'],
            port=self.cm.get_config('redis')['port']
        )
        if not r:
            print 'Redis服务未启动'
        else:
            print 'Redis服务正常'
            # 处理当前任务
            cur_task = r.rpoplpush(queue_data, queue_back)
            while cur_task is not None:
                # print cur_task
                is_success, rows = self.db.save(sql, eval(cur_task))
                if is_success:
                    # 提交成功, 清空备份队列
                    r.delete(queue_back)
                cur_task = r.rpoplpush(queue_data, queue_back)
            print '队列中没有要处理的任务'

    def get_sql(self):
        table_name = '%sresult' % self.cm.get_config('table')[0]['song']['prefix']
        sql_data_save = ("INSERT INTO %s " % table_name) + "(`sid`, `author`, `sname`, `counts`, `durl`) " \
                                                           "VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
                                                           "counts=counts+1;"
        return sql_data_save