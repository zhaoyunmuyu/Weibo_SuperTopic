'''

 Filename:  multiprocesses.py
 Description:  多进程爬虫主程序
 Created:  2022年04月19日 16时51分
 Author:  Li Shao

'''

import re
import json
import time
import requests
from config import Config
from multiprocessing import Pool
from data_process import extarct_container,extract_page
from topic_process import get_cates,get_topics

config = Config()
mydb = config.mydb

class loader():
    def __init__(self,page_num,header):
        self.page_num = page_num
        self.header = header
        self.pat = 'since_id=(.*)'

    def get_proxy(self):
        json = requests.get("http://127.0.0.1:5010/get").json()
        ip = json['proxy']
        http = 'http' if json['https'] == False else 'https'
        return {http:ip}

    def get_weibo(self,base_url):
        i = 1
        error_time = 0
        while i <= self.page_num:
            try:
                proxy = self.get_proxy()
                r=requests.get(base_url,headers=self.header,proxies=proxy,timeout=20)
                ori_data=json.loads(r.text)
                if i == 1:
                    container_info = extarct_container(ori_data)
                    container_col = mydb[container_info['container_name']]
                    container_col.delete_many({})
                    container_col.insert_one(container_info)
                    print('INFO:获取超话:',container_info['container_name'])
                lastpage,weibo = extract_page(ori_data)
                container_col.insert_many(weibo)
                error_time = 0
            except Exception as e:
                print(e)
                requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy[list(proxy.keys())[0]]))
                print("删除:",proxy[list(proxy.keys())[0]])
                print('获取数据失败:'+'INFO:IP:'+proxy[list(proxy.keys())[0]].split(':')[0]+',超话\"'+container_info['container_name']+'\"第{}页'.format(i))
                if error_time > 5:
                    # logging
                    break
                error_time += 1
                time.sleep(10)
                continue
            if i == 1:
                base_url = base_url + '&since_id=' + str(lastpage)
            print('INFO:IP:'+proxy[list(proxy.keys())[0]].split(':')[0]+',超话\"'+container_info['container_name']+'\"第{}页写入完毕'.format(i))
            base_url=re.sub(self.pat,'since_id='+str(lastpage),base_url)
            i += 1
            time.sleep(4)
        return

if __name__  == '__main__':
    load = loader(config.page_num,config.header)
    containers = {}
    urls = []
    # 获取类别
    cates = get_cates(config)
    # 获取各类别排名
    result = get_topics(config)
    for cate in config.cates_name:
        topics = result.get(cate)
        container = []
        for i in range(1,config.rank_num+1):
            topic_name = topics[str(i)].get('display_name')
            if len(config.target_topic) == 0:
                topic_id = topics[str(i)].get('topic_id')
                container.append(topic_name)
                topic_col = config.mydb[topic_name]
                base_url='''https://m.weibo.cn/api/container/getIndex?containerid={id}'''
                url = base_url.format(id=topic_id)
                urls.append(url)
            else:
                if topic_name in config.target_topic:
                    topic_id = topics[str(i)].get('topic_id')
                    container.append(topic_name)
                    topic_col = config.mydb[topic_name]
                    base_url='''https://m.weibo.cn/api/container/getIndex?containerid={id}'''
                    url = base_url.format(id=topic_id)
                    urls.append(url)
        containers[cate] = container
    pool = Pool(processes = config.process_num)
    pool.map(load.get_weibo, urls)
    print("Finish:获取超话:",containers)