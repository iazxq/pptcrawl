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
import func
import os
from dmoz.logger import logger



class DmozSpider(CrawlSpider):
    name="ppt"
    #allowed_domains = ['www.sjbz.org']
    start_urls = [
        "http://www.google.cn"
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
        #每次100个，下次修改start为start+100即可
        start = 1
        allSize = [{'size':'480x720','page':7},
                   {'size':'960x800','page':13},
                   {'size':'640x960','page':21},
                   {'size':'640x480','page':12},
                   {'size':'480x800','page':9},
                   {'size':'854x480','page':2},
                   {'size':'480x640','page':3},
                   {'size':'480x360','page':2},
                   {'size':'360x640','page':6},
                   {'size':'320x480','page':21},
                    {'size':'320x240','page':7},
                    {'size':'240x400','page':3},
                    {'size':'240x320','page':11},
                    {'size':'480x854','page':9},
                    {'size':'960x854','page':9}]
        for size in allSize:
            self.size = size['size']
            end = 1
            yield Request('http://www.sjbz.org/', callback=self.parse_list)

    #抓取列表页
    def parse_list(self,response):
        lasturl = self.readfile()
        hxs = HtmlXPathSelector(response)
        urlList = hxs.select('//div[@class="sy_m1_r FR"]/ul/li/div[@class="pic"]/a/@href').extract()
        for url in urlList:
            if url ==lasturl:
                break
            else:
                yield Request(url, callback=self.parse_item)
        self.writefile(urlList[0])

    #抓取详细页
    def parse_item(self,response):
        #logger.info('status:%s-%s'%(response.url,response.status))
        #如果页面转向了，则不管了
        #if 200 != response.status:
        #    return

        hxs = HtmlXPathSelector(response)
        item = DmozItem()
        item['title'] =  hxs.select('//div[@class="m_L2 FL"]/h2/text()').extract()[0]
        item['pic'] = hxs.select('//img[@id="bigimg"]/@src').extract()[0]
        item['category'] = response.url.split('/')[-2]
        item['size'] = self.size
        item['tags'] = ''
        item['description'] = item['title']
        sourceid = response.url.split('/')[-1].split('.')[0].split('_')[0]
        item['sourceid'] = sourceid
        nextUrl = hxs.select('//div[@class="page"]/ul/li/a/@href').extract()[-1]
        print('nextUrl =%s'% nextUrl)
        if nextUrl != '#':
            nextUrl = response.url[:response.url.rindex('/')+1] + nextUrl
            yield Request(nextUrl,callback=self.parse_item)

        logger.info('process finished :%s'%response.url)
        yield item


SPIDER = DmozSpider()


