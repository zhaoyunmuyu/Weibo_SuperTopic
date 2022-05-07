'''

 Filename:  data_process.py
 Description:  json处理函数
 Created:  2022年04月18日 16时51分
 Author:  Li Shao

'''

import time
import json
import requests
from w3lib.html import remove_tags

# 超话信息
def extarct_container(ori_data):
    container_id = ori_data.get('data').get('pageInfo').get('oid').split(':')[1]
    container_name = ori_data.get('data').get('pageInfo').get('title_top')
    container_describe = ori_data.get('data').get('pageInfo').get('desc')
    container_info = ori_data.get('data').get('pageInfo').get('desc_more')[0]
    container_sub = ori_data.get('data').get('pageInfo').get('portrait_sub_text')
    return {'type':'describe','container_id':container_id,'container_name':container_name,
            'container_describe':container_describe,'container_info':container_info,
            'container_sub':container_sub}

# 按页读取微博信息
def extract_page(ori_data):
    weibo = []
    lastPage = ori_data.get('data').get('pageInfo').get('since_id')
    for item in ori_data.get('data').get('cards'):
        if 'card_group' in item:
            temp = item.get('card_group')
            for item in temp:
                if 'mblog' in item:
                    blogData = item.get('mblog')
                    text = remove_tags(blogData.get('text').replace('全文', ''))
                    # 处理长文本微博
                    if blogData.get('isLongText') == 1:           
                        id = blogData.get('id')
                        time.sleep(1)
                        try:
                            text_url = 'https://m.weibo.cn/statuses/extend?id='+id
                            text_r=requests.get(text_url)
                            long_text = json.loads(text_r.text).get('data').get('longTextContent')
                            text = remove_tags(long_text)
                        except:
                            pass
                    text.replace('网页链接', '')
                    # 点赞评论转发
                    attitudes_count = blogData.get('attitudes_count')
                    comments_count = blogData.get('comments_count')
                    reposts_count = blogData.get('reposts_count')
                    # 时间
                    created_at = blogData.get('created_at')
                    latest_update = blogData.get('latest_update')
                    # 用户
                    user_id = blogData.get('user').get('id')
                    user_name = blogData.get('user').get('screen_name')
                    follow_count = blogData.get('user').get('follow_count')
                    followers_count = blogData.get('user').get('followers_count')
                    verified = blogData.get('user').get('verified')
                    result = {'type':'weibo','text':text,'created_at':created_at,'latest_update':latest_update,
                              'attitudes_count':attitudes_count,'comments_count':comments_count,'reposts_count':reposts_count,
                              'user':{'user_id':user_id,'user_name':user_name,'follow_count':follow_count,
                              'followers_count':followers_count,'verified':verified}}
                    # 图片
                    pic_num = blogData.get('pic_num')
                    if pic_num != 0:
                        pic_url = []
                        for item in blogData.get('pics'):
                            pic_url.append(item.get('large').get('url'))
                        result['pic'] = {'pic_num':pic_num,'pics':pic_url}
                    weibo.append(result)
    return lastPage,weibo


if __name__ == '__main__':
    # config = Config()
    # inf1=pd.DataFrame(inf,columns=['发布时间','内容'])
    # inf1.to_csv('daily_comment.csv',index=False,encoding='gb18030')
    print(1)