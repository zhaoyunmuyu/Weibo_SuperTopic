'''

 Filename:  config.py
 Description:  程序相关配置
 Created:  2022年04月18日 16时51分
 Author:  Li Shao

'''

import random
import pymongo

class Config():
    def __init__(self):
        head_list=["Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
            "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
            "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
            "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
        ]
        ip=['114.101.42.16:65309',
            '220.179.255.7:8118',
            '103.44.145.182:8080',
            '115.223.7.110:80']
        self.proxy={'http':random.choice(ip)}
        self.header={'user-agent':random.choice(head_list)}
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["weibo_0418"]
        self.page_num = 100
    
    def show_config(self):
        for name,value in vars(self).items():
            print(name+":",value)
        print(self.myclient.list_database_names())