# Weibo_SuperTopic
https://github.com/zhaoyunmuyu/Weibo_SuperTopic
本项目可以爬取微博超话信息，并通过NLP方法对超话进行分析。

## Author
Lishao SCU, 2022/4/25

## 代码结构
|--Weibo_SuperTopic
|----\pic              保存生成后的词云图片文件
|----lda.py            超话主题聚类函数
|----config.py         程序配置信息
|----word_cloud.py     生成对应超话的词云
|----cover_rate.py     计算超话用户之间重合度
|----data_process.py   处理获取到的JSON数据函数
|----multiprocess.py   多进程爬虫主程序
|----topic_process.py  获取最新的热榜超话排名
|----hit_stopwords.txt 哈工大停用词表

## 环境依赖
requests, pymongo, matplotlib, wordcloud, w3lib, jieba

## 使用
- 1. 修改config.py中的cates_name等参数，确定爬取的类别；
- 2. 运行ProxyPool爬虫代理IP池程序和MongoDB；
- 3. 运行multiprocess.py获取数据；
- 4. 修改相关信息，运行相关文本分析代码分析数据；

## 设计说明

### 爬虫部分
- 1. 爬虫目标网址为微博的手机端网址：m.weibo.cn;
- 2. 通过对网页数据包的分析，可以得到多个有用的API接口：
  - 2.1 获取超话类别的ID: https://huati.weibo.cn/aj/discovery/cates
  - 2.2 获取对应类别超话的排名以及其ID: https://huati.weibo.cn/aj/discovery/rank?
  - 2.3 按页获取超话中微博信息: https://m.weibo.cn/api/container/getIndex?containerid=xxx, 其中下一页的container_id可以在上一页的json数据中获取到
  - 2.4 除明星类别外，其他类别都按照热度顺序进行排序，默认选取热度前十的超话进行爬取，对明星类别进行额外外处理。
  - 2.5 游戏类别的子类无法在2.1所示的接口中获取，暂时通过手动获取。
- 3. 爬虫使用**ProxyPool爬虫代理IP池**所提供的代理服务器进行多进程爬取，详情可参考[document](https://proxy-pool.readthedocs.io/zh/latest/) [![Documentation Status](https://readthedocs.org/projects/proxy-pool/badge/?version=latest)](https://proxy-pool.readthedocs.io/zh/latest/?badge=latest)
- 4. 2.3中接口不能够获取较长微博的全部文本信息，进行了额外的处理。

### 数据存储
- 1. 数据存储使用MongoDB实现，数据库名等信息可以在config.py文件中进行修改。

### 文本分析
- 1. 生成超话词云
- 2. 计算超话用户重合度
- 3. 超话话题LDA聚类（待实现）