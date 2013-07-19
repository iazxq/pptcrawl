# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import sys
import json
import codecs
import pickle
import urllib
import os
import datetime

import imagefactory
from logger import logger
from scrapy import log
import pymongo
from gallary import Gallary
import func
import traceback

class DmozPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
    	import socket
        socket.setdefaulttimeout(30)
        log.msg(u'start process data...')
        try:
            pic_file=''

            #必须有标题才能下载图片
            if item.get('title',''):
                #下载图片并生成缩略图
                #判断路径是否存在，同时是否是图片地址
                if item['pic'] and item['pic'].lower().endswith(('.jpg','.gif','.png')):
                    try:
                        save_path = 'up/' + item['sourceid']
                        item['title'] = item['title'].replace('/',' ').replace('*','x').replace(':','').replace('\\','').replace('?','').replace('<','').replace('>','').replace('|','').replace('"','')
                        new_filename = item['title'] +'_' + item['size']+'_' + func.get_new_filename(item['pic'])
                        pic = new_filename

                        if not os.path.exists(save_path):
                            os.makedirs(save_path)
                        pic_file = os.path.join(save_path,pic).replace('\\','/')

                        urllib.urlretrieve(item['pic'],pic_file)

                    except:
                        print(traceback.format_exc())
                      	
            log.msg(u'pic process finished')
        except Exception as e:
            log.msg(u'failed:%s'%(e.message,))
            traceback.print_exc()
            pass

        return item
