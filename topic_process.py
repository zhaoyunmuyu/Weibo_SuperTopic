'''

 Filename:  topic_process.py
 Description:  发现最新的热榜超话排名
 Created:  2022年04月18日 10时16分
 Author:  Li Shao

'''

import json
import requests
import time
from config import Config

# 查询类别Cates的ID
def get_cates(config):
    cate_url = 'https://huati.weibo.cn/aj/discovery/cates'
    r=requests.get(cate_url,headers=config.rank_headers)
    cate_data=json.loads(r.text).get('data')
    cate_data.pop('is_party')
    cate_data.pop('lbs_cate')
    cat_dic = {}
    config.cate_col.delete_many({})
    for item in cate_data['cates']:
        child = {}
        # 处理游戏类别
        if item.get('name') == '游戏':
            game_url = 'https://huati.weibo.cn/aj/discovery/rank?cate_id={id}&page=1&topic_to_page=&from=&wm=&isvivo=false'.format(id = item.get('id'))
            r=requests.get(game_url,headers=config.rank_headers)
            for item in json.loads(r.text).get('data').get('top_one'):
                chi_id = item.get('ctg_id')
                chi_name = item.get('short_rank_name')
                child[chi_name] = chi_id
                config.cate_col.insert_one({'name':chi_name,'id':chi_id})
        else:
            for chi in item.get('child'):
                if chi.get('id') != 0:
                    chi_name = chi.get('name')
                    chi_id = chi.get('id')
                    child[chi_name] = chi_id
                    config.cate_col.insert_one({'name':chi_name,'id':chi_id})
        cat_dic[item.get('name')] = {'total':1,'id':item.get('id'),'child':child}
        config.cate_col.insert_one({'name':item.get('name'),'id':item.get('id')})
    #config.cate_col.insert_one(cate_data)
    return cat_dic

# 查询对应类别的ID
def get_topics(config):
    results = {}
    for temp in config.cates_name:
        print('INFO:获取超话类别:',temp)
        topic_col = config.mydb[temp]
        query = {"name": temp}
        if temp == '明星':
            topics = get_topics_stars(config)
        else:
            x = config.cate_col.find(query)[0]
            id = x['id']
            base_url='''https://huati.weibo.cn/aj/discovery/rank?cate_id={id}&page=1&topic_to_page=&block_time=0&star_type=star&from=&wm=&isvivo=false'''
            url = base_url.format(id=id)
            try:
                r=requests.get(url,headers=config.rank_headers)
                topic_data=json.loads(r.text).get('data').get('list')
            except Exception as e:
                print('获取数据失败:',base_url,'Error:',e.__class__.__name__,e)
            topics = {}
            for item in topic_data:
                display_name = item.get('display_name')
                fans_count = item.get('fans_count')
                status_count = item.get('status_count')
                topic_id = item.get('page_id')
                rank = item.get('rank_no')
                topic = {'rank':rank,'display_name':display_name,'topic_id':topic_id,
                         'status_count':status_count,'fans_count':fans_count}
                topics[str(rank)] = topic
        topics['time']=time.time()
        topic_col.insert_one(topics)
        results[temp] = topics
        time.sleep(2)
    return results

# 单独处理明星类
def get_topics_stars(config):
    cate_url = 'https://huati.weibo.cn/aj/discovery/rank?cate_id=2&page={id}'
    topics = {}
    while 1:
        for id in range(1,11):
            url = cate_url.format(id = id)
            try:
                r=requests.get(url,headers=config.rank_headers)
                cate_data=json.loads(r.text).get('data').get('list')
            except Exception as e:
                print('获取数据失败:',url,'Error:',e.__class__.__name__,e)
            for item in cate_data:
                rank = item.get('rank_no')
                if (rank <= 20) & (rank not in topics.keys()):
                    display_name = item.get('display_name')
                    fans_count = item.get('fans_count')
                    status_count = item.get('status_count')
                    topic_id = item.get('page_id')
                    rank = item.get('rank_no')
                    topic = {'rank':rank,'display_name':display_name,'topic_id':topic_id,
                            'status_count':status_count,'fans_count':fans_count}
                    topics[rank] = topic
        time.sleep(2)
        if len(topics.keys()) == 20:
            sorted(topics.items(), key=lambda x: x[0])
            result = {}
            for no in topics.keys():
                result[str(no)] = topics[no]
            return result

if __name__ == '__main__':
    config = Config()
    get_cates(config)
    get_topics(config)