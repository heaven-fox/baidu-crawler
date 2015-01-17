# coding: utf-8

from crawler.conf.cm import ConfigManager
import redis
cm = ConfigManager()


def cleanup():
    r = redis.Redis(
        host=cm.get_config('redis')['host'],
        port=cm.get_config('redis')['port']
    )
    if not r:
        print 'Redis服务未启动'
    else:
        print 'Redis服务正常'
        # 清空redis错误数据
        print '开始清理redis垃圾数据'
        queue_data = cm.get_config('taskqueue')['data']
        queue_back = cm.get_config('taskqueue')['backup']
        r.delete(queue_data)
        r.delete(queue_back)
        print '清理完成'