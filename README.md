## 基于 scrapy 爬虫框架对百度实时热点新闻内容进行爬取

#### 实现的功能 
- 爬取百度实时热点话题首页新闻字数最多的内容
- 根据自身项目需要，过滤出命中所给关键词的热点话题内容（参考代码 spider文件夹的keywords.csv）
- 对爬取过的热点话题存储下次不在爬取（spider文件夹中的black文件，项目部署在linux上，通过crontab小时执行爬取任务）
- 爬取内容存储到mongodb中 

#### linux 环境配置
    pip install newspaper
    pip install scrapy     

#### 程序执行 
    cd craw3.0/Headlines/Headlines
    python main.py 

    
