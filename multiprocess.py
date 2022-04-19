import re
import json
import time,random
import requests
from config import Config
from multiprocessing import Pool
from data_process import extarct_container,extract_page
from topic_process import get_cates,get_topics

config = Config()
myclient = config.myclient

class loader():
    def __init__(self,page_num,header,proxy):
        self.page_num = page_num
        self.header = header
        self.proxy = proxy
        self.pat = 'since_id=(.*)'

    def get_weibo(self,base_url):
        mydb = myclient["weibo_0419"]
        i = 1
        while i <= self.page_num:
            try:
                r=requests.get(base_url,headers=self.header,proxies=self.proxy)
                ori_data=json.loads(r.text)
                if i == 1:
                    container_info = extarct_container(ori_data)
                    container_col = mydb[container_info['container_name']]
                    container_col.insert_one(container_info)
                    print('INFO:获取超话:',container_info['container_name'])
                lastpage,weibo = extract_page(ori_data)
                container_col.insert_many(weibo)
            except Exception as e:
                print('获取数据失败:',base_url)
                time.sleep(30)
                continue
            if i == 1:
                base_url = base_url + '&since_id=' + str(lastpage)
            print('INFO:超话\"'+container_info['container_name']+'\"第{}页写入完毕'.format(i))
            base_url=re.sub(self.pat,'since_id='+str(lastpage),base_url)
            i += 1
            time.sleep(random.randint(3,5))

if __name__  == '__main__':
    load = loader(config.page_num,config.header,config.proxy)
    containers = {}
    urls = []
    cates = get_cates(config)
    result = get_topics(config)
    for cate in config.cates_name:
        topics = result.get(cate)
        container = []
        for i in range(1,config.rank_num+1):
            topic_name = topics[str(i)].get('display_name')
            topic_id = topics[str(i)].get('topic_id')
            container.append(topic_name)
            topic_col = config.mydb[topic_name]
            base_url='''https://m.weibo.cn/api/container/getIndex?containerid={id}'''
            url = base_url.format(id=topic_id)
            urls.append(url)
        containers[cate] = container
    pool =Pool(processes = 5)
    pool.map(load.get_weibo, urls)
    print("Finish:获取超话目录:",containers)