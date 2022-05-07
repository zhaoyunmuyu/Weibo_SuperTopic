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
        self.mydb = self.myclient["weibo_0507"]
        self.cate_col = self.mydb["cates_id"]
        self.page_num = 50
        self.rank_num = 10
        self.process_num = 5
        self.all_cates = ['cates_id','影视综','游戏','吐槽','体育运动','日韩动漫','虚拟偶像','动漫角色','明星','红人','LPL','校园']
        self.cates_name = ['影视综','本地','游戏','体育运动','日韩动漫','虚拟偶像','动漫角色','明星','红人','LPL']                             # 获取超话类别
        self.target_topic = []                # 选取类别中的某些超话，全选则为空

    def get_proxy(self):
        json = requests.get("http://127.0.0.1:5010/get").json()
        ip = json['proxy']
        http = 'http' if json['https'] == False else 'https'
        return {http:ip}

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
    proxy = config.get_proxy()
    print('INFO:IP:'+proxy[list(proxy.keys())[0]].split(':')[0])
    r= requests.get("http://www.baidu.com",headers=config.header,proxies=config.get_proxy())
    print(r)