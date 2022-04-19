'''

 Filename:  main.py
 Description:  爬虫主程序
 Created:  2022年04月18日 16时51分
 Author:  Li Shao

'''

import re
import json
import requests
import time,random
from config import Config
from data_process import extarct_container,extract_page
from topic_process import get_cates,get_topics

def get_weibo(base_url,container_col,config):
    for i in range(1,config.page_num+1):
        try:
            r=requests.get(base_url,headers=config.header) # proxy = config.proxy
            ori_data=json.loads(r.text)
        except Exception as e:
            print('获取数据失败:',base_url,'Error:',e.__class__.__name__,e)
        if i == 1:
            container_info = extarct_container(ori_data)
            container_col.insert_one(container_info)
            print('INFO:获取超话:',container_info['container_name'])
        lastpage,weibo = extract_page(ori_data)
        container_col.insert_many(weibo)
        if i == 1:
            base_url = base_url + '&since_id=' + str(lastpage)
        print('INFO:第{}页写入完毕'.format(i))
        base_url=re.sub(pat,'since_id='+str(lastpage),base_url)
        time.sleep(random.randint(3,5))
        
if __name__ == '__main__':
    config = Config()
    containers = {}
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
            pat='since_id=(.*)'
            base_url='''https://m.weibo.cn/api/container/getIndex?containerid={id}'''
            url = base_url.format(id=topic_id)
            get_weibo(url,topic_col,config)
        containers[cate] = container
    print("Finish:获取超话目录:",containers)
