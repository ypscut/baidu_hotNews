# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class HeadlinesItem(Item):
    keywords = Field()
    snap = Field()
    title = Field()
    text =Field()
    time = Field()



class HeadlinesItem(Item):
    keyword=Field()
    hot_topic =Field()
    relevance=Field()
    title = Field()
    words = Field()
    #Originality = Field()
    #publish_time =Field()
    rank_num = Field()
    search_title = Field()
    url = Field()
    content = Field()
    create_time =Field()
