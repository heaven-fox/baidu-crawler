# coding: utf-8

from crawler.conf.cm import ConfigManager
from crawler.db.dbmanager import DBManager
cm = ConfigManager()
db = DBManager()


def setup_env():
    print '检查环境'
    # 创建歌曲url记录表
    table_name = '%sresult' % cm.get_config('table')[0]['song']['prefix']
    # print 'hello, ', table_name
    sql_is_table_exist = "show tables like '%s'" % table_name
    if db.query_table_exist_with_sql(sql_is_table_exist) == 0:
        print "\t建表%s" % table_name,
        sql_execute_result = """
          CREATE TABLE `%s` (
              `id` INT(11) unsigned NOT NULL AUTO_INCREMENT,
              `sid` VARCHAR(20) NOT NULL DEFAULT '',
              `author` VARCHAR(20) NOT NULL DEFAULT '',
              `sname` VARCHAR(50) NOT NULL DEFAULT '',
              `counts` INT(10) NOT NULL DEFAULT 0,
              `durl` VARCHAR(250) NOT NULL DEFAULT '',
              PRIMARY KEY(`id`),
              UNIQUE KEY `sid` (`sid`)
          ) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
          """ % table_name
        db.create_table(sql_execute_result)
        print '\t建表成功'
    else:
        print '\t表%s已存在' % table_name
    db.close()
    print '环境搭建完成'