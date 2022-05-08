'''

 Filename:  cover_rate.py
 Description:  分析两个超话之间的用户重复度,生成结构图
 Created:  2022年04月25日 10时35分
 Author:  Li Shao

'''

import csv
import networkx as nx
import pandas as pd
from config import Config
import matplotlib.pyplot as plt

config = Config()
mydb = config.mydb

def get_user(topic_col):
    user_name = []
    query = {"type": 'weibo'}
    for item in topic_col.find(query):
        user = item.get('user').get('user_name')
        user_name.append(user)
    if len(user_name) == 0:
        return 0
    return set(user_name)

def compare(topics:list):
    topic1_col = mydb[topics[0]]
    topic2_col = mydb[topics[1]]
    topic1_usr = get_user(topic1_col)
    topic2_usr = get_user(topic2_col)
    # print(topics[0]+':',len(topic1_usr),topics[1]+':',len(topic2_usr))
    res = list(topic1_usr & topic2_usr)
    # print('cover_user:',len(res),'cover_rate:',float(len(res)*2/(len(topic1_usr)+len(topic2_usr))))
    return len(topic1_usr),len(topic2_usr),res,float(len(res)*2/(len(topic1_usr)+len(topic2_usr)))

def compare_all():
    topic_list = config.mydb.list_collection_names(session=None)
    headers = ['topic1','topic1_num','topic2','topic2_num','cover_user','cover_num','cover_rate']
    with open('./cover_rate.csv', 'a+', newline='', encoding='GBK') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in range(len(topic_list)):
            topic1 = topic_list[i]
            topic1_col = mydb[topic1]
            if get_user(topic1_col) == 0:
                continue
            for temp in range(i+1,len(topic_list)):
                topic2 = topic_list[temp]
                topic2_col = mydb[topic2]
                if get_user(topic2_col) == 0:
                    continue
                topics = [topic1,topic2]
                topic1_num,topic2_num,cover_user,cover_rate = compare(topics)
                cover_num = len(cover_user)
                writer.writerow([topic1,topic1_num,topic2,topic2_num,cover_user,cover_num,cover_rate])
            print(topic1)

def make_network(limit_rate:float):
    g=nx.Graph(date="4.25",name="超话关系图")
    plt.rcParams['font.sans-serif'] = [u'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    topic_dict = {}
    for cate in config.all_cates:
        if cate == 'cates_id':
            continue
        cate_col = mydb[cate]
        x = cate_col.find()[0]
        for i in range(1,config.rank_num+1):
            topic_dict[x[str(i)].get('display_name')] = cate
            ## 其他属性   
        # topic_dict['咒术回战'] = '日韩动漫'
    df = pd.read_csv('cover_rate.csv',encoding='GBK')
    df2 = df[[float(rate) > limit_rate for rate in df['cover_rate']]]
    df2 = df2.reset_index(drop=True)
    for i in range(0,len(df2)):
        topic1 = str(df2.at[i,'topic1'])
        topic2 = str(df2.at[i,'topic2'])
        topic1_num = int(df2.at[i,'topic1_num'])
        topic2_num = int(df2.at[i,'topic2_num'])
        cover_num = int(df2.at[i,'cover_num'])
        cover_rate = float(df2.at[i,'cover_rate'])
        g.add_node(topic1,cate=topic_dict[topic1],usr_num=topic1_num)
        g.add_node(topic2,cate=topic_dict[topic2],usr_num=topic2_num)
        g.add_edge(topic1,topic2,num=cover_num,weight=cover_rate)
    pos = nx.shell_layout(g)
    color = ['red','yellow','blue','green','pink','orange','aqua','violet']
    color_dict = {}
    for node,data in g.nodes.items():
        cate = data['cate']
        usr_num = data['usr_num']
        try:
            cate_color = color_dict[cate]
        except:
            color_dict[cate] = color[0]
            color.pop(0)
            cate_color = color_dict[cate]
        nx.draw_networkx_nodes(g,pos=pos,nodelist=[node],alpha=0.6,node_color=cate_color,node_size=usr_num*6,linewidths=1)
    for edge,data in g.edges().items():
        weight = data['weight']
        nx.draw_networkx_edges(g,pos=pos,edgelist=[edge],width=weight*10,edge_color='k')
    # edge_labels = nx.get_edge_attributes(g,'num')
    # nx.draw_networkx_edge_labels(g,pos,edge_labels=edge_labels,font_size=10)
    nx.draw_networkx_labels(g,pos=pos,font_size=15,font_color='k',alpha=1)
    # nx.draw(g,pos=pos,node_size=1000,node_color="r",edge_color="g")
    plt.show()  

if __name__ == '__main__':
    # topics = ['Tian高天亮','fpx']
    # result = compare(topics)
    # compare_all()
    make_network(0.04)


    
        

