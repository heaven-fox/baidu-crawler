# coding: utf-8

import simplejson as json


# 序列化数据，便于网络传输
class DataSerialization():
    def __init__(self):
        # 完成初始化工作
        pass

    def data_to_json(self, data):
        # 数据转成json格式
        json_data = json.dumps(data)
        # print 'json data: ', json_data
        return json_data

    def json_to_data(self, json_data):
        # 解析json格式数据
        data = json.loads(json_data)
        # print 'data: ', data
        return data