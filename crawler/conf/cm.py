# coding: UTF-8


class ConfigManager:
    def __init__(self):
        # self.env = "production"
        self.env = "development"
        self.config = {
            "development": {
                "mysql": {
                    "host": "127.0.0.1",
                    "user": "root",
                    "passwd": "asd123",
                    "db": "baidu",
                    "charset": "utf8"
                },
                "redis": {
                    "host": "127.0.0.1",
                    "port": 6379
                },
                "taskqueue": {
                    "data": "data_list",
                    "backup": "backup_list"
                },
                "table": [
                    {
                        "song": {
                            "limit": 1000000,
                            "prefix": "baidu_"
                        }
                    }
                ],
                "dir": {
                    "path": "out/"
                },
                "target": {
                    "authors": {"张国荣", "邓紫棋" ,"陈慧娴", "刘若英", "姚贝娜"}
                }
            }
        }

    def get_dbconfig(self):
        db_config = self.config[self.env]["mysql"]
        return db_config

    def get_config(self, name):
        config = self.config[self.env][name]
        return config