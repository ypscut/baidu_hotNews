# coding=UTF-8
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from Headlines.items import HeadlinesItem
from scrapy.http import  Request
import requests
import time
from newspaper import Article
from scrapy.crawler import CrawlerProcess
import  csv
import  re
import os


class HeadlinesSpider(CrawlSpider):
    name = "Headlines"
    allowed_domains = ["top.baidu"]
    start_urls = ["http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b341_c513"]
    #start_urls = ["http://top.baidu.com/buzz?b=1&c=513","http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1_c513","http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513"]
    hot_topics=[]

    def parse(self, response):
        selector = Selector(response)

        hot_topics = selector.xpath('//a[@class="list-title"]/text()').extract()
        raw_urls = selector.xpath('//a[@class="icon-search icon-xiang-imp"]/@href').extract()
        urls=[]
        for i in range(len(raw_urls)):
            urls.append(str("http://top.baidu.com") + raw_urls[i][1:])
        assert(len(hot_topics)==len(urls))
        keyword = []
        hit_urls = []
        hit_topics = []

        path = os.getcwd()
        data_path = os.path.join('spiders/keywords.csv')
        hit_dic = {}
        #data_path = os.path.join('keywords.csv')
        with open(data_path,'r',encoding="utf-8_sig") as f:
            f_csv = csv.reader(f)
            pop = set()
            for word in f_csv:
                pattern=re.compile(u'([\u4e00-\u9fa5]{0,5}?(?:%s))'%word[0])
                for i in range(len(hot_topics)):
                    if i not in pop:
                        s = pattern.search(hot_topics[i])
                        if s:
                            keyword.append(word[0])
                            hit_urls.append(urls[i])

                            hit_topics.append(hot_topics[i])
                            temp_ = {word[0]:urls[i]}
                            hit_dic[hot_topics[i]] = temp_
                            pop.add(i)
                        else:
                            continue


        for k ,v in  hit_dic.items():
            with open('spiders/used_Topics','r') as f:
                file = f.read().split("\n")[:-1]
                if k not in file:

                    for k1,v1 in v.items():
                        item = HeadlinesItem(keyword=k1,hot_topic=k)

                        item['relevance']=0
                        request = Request(url=v1,callback=self.parse_keywords,meta={'item':item},dont_filter=True)
                        yield request
                    with open('spiders/used_Topics','a+') as f:
                        f.writelines(k+'\n')
                print('a')

    def parse_keywords(self,response):
        #response = response.replace(body=response.body.replace('<em>', ''))
        item = response.meta['item']
        selector = Selector(response)
        news_snap_url = selector.xpath('//*[@class="result c-container "]')
        black_path = os.path.join('spiders/black.csv')

        for result in  news_snap_url:
            black_word = False
            search_title = result.xpath('.//h3/a/text()').extract()[-1]
            search_title_reg = re.sub(u"(⊙o⊙)|[\/\!\\\\_,$%^*\"\'\[\]]+|[——！。？、~@#￥……&（）'()-:;<=>?@^_`|}~·×ΔΨγμφ—‘’“””…′∈′｜℃Ⅲ↑→［∪φ≈──■▲　、。〈〉《》》）」『』【】〔〕︿！＃＄％＆＇（）÷＊＋ξ－β．／：；＜±λ＝″☆（－［｛＞？＠［－］∧′＿｛－｜｝～±＋￥ ]+", u"",search_title)
            search_title_reg = re.sub(u"\s+", u" ",search_title_reg)
            url = result.xpath('.//h3/a/@href').extract()[0]
            rank_num = result.xpath('.//@id').extract()[0]
            search_title_reg.encode("utf8")

            with open(black_path,'r',encoding="utf-8_sig") as f:
                black_csv = csv.reader(f)
                for w in black_csv:
                    pattern=re.compile(u'([\u4e00-\u9fa5]{0,5}?(?:%s))'%w[0])
                    b = bool(pattern.search(search_title_reg))
                    if pattern.search(search_title_reg):     #  if hit black words, break
                        black_word = True
                        break
            if black_word:
                continue
            else:
                article= Article(url, language='zh')
                article.download()
                article.parse()
                article_= article.text
                if len(article_)<50:
                    continue
                title_= article.title
                item['url'] = url
                item['create_time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['rank_num'] = rank_num
                item['search_title'] = search_title
                try:
                    item['title']= title_
                    item['content']= article_.replace("\n", "")
                    item['words'] = len(article_.replace("\n", ""))

                except Exception:
                    continue
                yield item


if __name__=='__main__':
    process = CrawlerProcess({'USER_AGENT':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'})
    process.crawl(HeadlinesSpider)
    process.start()



