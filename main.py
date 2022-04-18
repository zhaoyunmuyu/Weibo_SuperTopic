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


config = Config()
# for name OR container_id in text
# https://huati.weibo.cn/discovery/super
container_col = config.mydb["containers"]

pat='since_id=(.*)'
base_url='''https://m.weibo.cn/api/container/getIndex?containerid=1008082daf12cb79491a80017ae2546cc6f49f'''
for i in range(1,config.page_num+1):
    try:
        r=requests.get(base_url,headers=config.header) # proxy = config.proxy
        ori_data=json.loads(r.text)
        if i == 1:
            container_info = extarct_container(ori_data)
            container_col.insert_one(container_info)
            print('INFO:获取超话:',container_info['container_name'])
        lastpage,weibo = extract_page(ori_data)
        weibo_col = config.mydb[container_info['container_name']]
        weibo_col.insert_many(weibo)
        if i == 1:
            base_url = base_url + '&since_id=' + str(lastpage)
        print('INFO:第{}页写入完毕'.format(i))
        base_url=re.sub(pat,'since_id='+str(lastpage),base_url)
        time.sleep(random.randint(3,5))
    except Exception as e:
        print('获取数据失败:',base_url,'Error:',e.__class__.__name__,e)