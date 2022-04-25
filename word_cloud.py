'''

 Filename:  worl_cloud.py
 Description: 生成超话的词云
 Created:  2022年04月22日 10时35分
 Author:  Li Shao

'''

import os
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from config import Config

def word_cloud(config,cover=0):
    for item in config.mydb.list_collection_names(session=None):
        try:
            if(make_wordcloud(item,cover)):
                print('生成:',item)
        except:
            continue

def make_wordcloud(topic:str,cover):
    config = Config()
    if (cover == 0) & (os.path.exists('./pic/'+topic+'.png')):
        print('已存在:',topic)
        return 0
    stopwords=open('./hit_stopwords.txt','r',encoding='utf-8').read()
    # jieba.load_userdict('./extend_jieba.txt')
    topic_col = config.mydb[topic]
    final = []
    for item in topic_col.find():
        if item['type'] == 'weibo':
            text = item['text']
            cuttext= jieba.cut(text)
            for seg in cuttext:
                    if seg[0] not in ['0','1','2','3','4','5','6','7','8','9']:
                        if seg not in stopwords:
                            li = [topic,'网页','链接','微博','视频','超话','全文','真的']
                            for i in jieba.cut(topic):
                                li.append(i)
                            if seg not in li:
                                final.append(seg)
    wordcloud = WordCloud(font_path=r"c:/Windows/Fonts/simsun.ttc",
                          background_color="white",
                          width=1000,
                          height=860,
                          margin=2).generate(" ".join(final))
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file('./pic/'+topic+'.png')
    return plt

if __name__ == '__main__':
    config = Config()
    # make_wordcloud('原神',cover=1).show()
    word_cloud(config)
