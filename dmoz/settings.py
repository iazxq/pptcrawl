# -*- coding: utf-8 -*-
# Scrapy settings for dmoz project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/0.12/topics/settings.html#std:setting-RANDOMIZE_DOWNLOAD_DELAY
#
from scrapy.settings.default_settings import DOWNLOAD_DELAY

BOT_NAME = 'dmoz'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['dmoz.spiders']
NEWSPIDER_MODULE = 'dmoz.spiders'
DEFAULT_ITEM_CLASS = 'dmoz.items.DmozItem'
USER_AGENT = 'Mozilla/5.0+(Windows+NT+6.1;+WOW64)+AppleWebKit/535.1+(KHTML,+like+Gecko)+Chrome/14.0.835.202+Safari/535.1'
ITEM_PIPELINES = [
'dmoz.pipelines.DmozPipeline',
]

#下载延迟
DOWNLOAD_DELAY = 1
#下载延迟采用随机数， between 0.5 and 1.5 * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True
#不允许转向
REDIRECT_MAX_TIMES=0
#同时放出的蜘蛛数
CONCURRENT_SPIDERS=1 #默认8
#每个蜘蛛最大同时发出的request数
CONCURRENT_REQUESTS_PER_SPIDER=2#默认8

