# -*- coding: utf-8 -*-
from scrapy.conf import settings
import pymongo
import logging
from scrapy.exceptions import DropItem

class HeadlinesSpider(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]
        #self.post.remove({})
        self.ids_seen = set()

    def process_item(self, item, spider):

        NewsInfo = dict(item)
        logging.info('insert title:' + item['title'])
        self.post.insert(NewsInfo)
        return item


'''
class NovelspiderPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        bookInfo = dict(item)
        self.post.insert(bookInfo)
        return item
'''