'''

 Filename:  config.py
 Description:  程序相关配置
 Created:  2022年04月18日 16时51分
 Author:  Li Shao

'''

import json
import time
import requests
import random
import pymongo
from data_process import extract_page

class Config():
    def __init__(self):
        head_list=["Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
            "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
            "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
            "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
        ]
        self.ip=['104.129.198.228:8800',
            '124.205.155.157:9090',
            '165.225.196.64:10605',
            '94.74.182.148:80',
            '202.44.193.250:8080',
            '93.157.163.66:35081',
            '95.0.168.50:1981',
            '112.78.14.167:3128']
        self.proxy={'http':random.choice(self.ip)}
        self.rank_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": r"_T_WM=2511c5ff3f99aa1a1b6807e77563e75c; WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=luicode%3D20000314%26lfid%3D126%26fid%3D100808ccb61d96c8f867d4f6c412e95c4f173a_-_feed%26uicode%3D10000011",   # 换成你的cookie
            "Host": "huati.weibo.cn",
            "Pragma": "no-cache",
            "Referer": "https://huati.weibo.cn/discovery/super",
            "sec-ch-ua-mobile": "?0",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",  # 换成你的user-agent
            "X-Requested-With": "XMLHttpRequest"
        }
        self.header={'user-agent':random.choice(head_list)}
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["weibo_0419"]
        self.cate_col = self.mydb["cates_id"]
        self.page_num = 300
        self.rank_num = 10
        # self.cates_name = ['日韩动漫','校园']
        self.cates_name = ['吐槽']
        
    def show_config(self):
        for name,value in vars(self).items():
            print(name+":",value)
        print(self.myclient.list_database_names())
    
    def test_ipPool(self):
        for ip in self.ip:
                proxy = {'http':ip}
                print('测试ip:'+ip)
                i = 0
                while i < 5:
                    try:
                        base_url='''https://m.weibo.cn/api/container/getIndex?containerid=1008083829ec9f6d5c6b53889bd24dfb2eac1c'''
                        r=requests.get(base_url,headers=self.header,proxies=proxy)
                        ori_data=json.loads(r.text)
                        _,_ = extract_page(ori_data)
                        print('IP:'+ip+' 获取数据成功')
                        i += 1
                        time.sleep(4)
                    except Exception as e:
                        print(e)
                        i += 1
                        print('IP:'+ip+' 获取数据失败')
                        time.sleep(4)
                        continue
    
if __name__ == '__main__':
    config = Config()
    config.test_ipPool()