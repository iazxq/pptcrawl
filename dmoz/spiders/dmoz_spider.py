# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from scrapy.http import Request
from dmoz.items import DmozItem
from urlparse import urljoin
import re
import time
from dmoz import func
import os
from dmoz.logger import logger
import simplejson
import urllib



class DmozSpider(CrawlSpider):
    name="ppt"
    #allowed_domains = ['www.sjbz.org']
    start_urls = [
        "http://www.baidu.com"
    ]


    def readfile(self):
        url = ''
        if os.path.exists('lasturl.txt'):
            f = open('lasturl.txt','r')
            url = f.read()
            f.close()
        return url

    def writefile(self,url):
        f = open('lasturl.txt','w')
        f.write(url)
        f.close()

    #抓取列表页
    def parse(self, response):
        q = u'小学语文'
        url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyADlwB_pCviey8204EeASlSEP2HaM3tgWc&cx=013036536707430787589:_pqjad5hr1a&alt=json&num=10&language=zh-cn&start=20&fileType=ppt&q=%s'%q
        yield Request(url, callback=self.parse_list)

    #抓取列表页
    def parse_list(self,response):
        hxs = HtmlXPathSelector(response)
        json = eval(response.body)
        items = json.get('items',None)
        if items:
            for i in items:
                item = DmozItem()
                item['title'] = unicode(i.get('title',''),'utf-8')
                item['link'] =unicode(i.get('link',''),'utf-8')
                item['snippet'] = unicode(i.get('snippet',''),'utf-8')

                newFile = os.path.join(os.getcwd(),'down/',func.get_new_filename(item['link'])).replace('\\','/')
                urllib.urlretrieve(item['link'],newFile)
                yield item




SPIDER = DmozSpider()


