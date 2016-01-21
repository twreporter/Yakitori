#! /usr/bin/python
# -*- coding: utf8 -*-

from datetime import datetime
import logging
import os
import pycurl
import json
import re
import sys
from StringIO import StringIO

reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(filename='/tmp/log/fetch.log',level=logging.INFO)

logging.info('fetch articles from atavist')

buffer = StringIO()

api = 'https://atavist.com/api/public/library.php?organization_id=60826&paginationLimit=100'
target_folder = '/tmp/twreporters/articles/'

logging.info('api: %s ', api)

c = pycurl.Curl()
cc = pycurl.Curl()
c.setopt(c.URL, api)
c.setopt(c.WRITEDATA, buffer)
c.perform()
result = buffer.getvalue()
records = json.loads(result, encoding="utf-8")

articles = []

fo = open("./articles", "w")
logging.debug('records from api: %s', json.dumps(records))

for i in records['stories']:
    pageBuffer = StringIO()
    fileName = i['slug']
    author = i['author_display']
    pub_date = i['pub_date']
    logging.info('get file: %s', fileName)
    cc.setopt(cc.URL, i['url'])
    cc.setopt(cc.WRITEDATA, pageBuffer)
    cc.perform()
    body = pageBuffer.getvalue()
    a = re.findall(r'<p>.+?<\/p>', body)
    story = ''.join(a)
    story = re.sub(r'<.+?>', r'', story)
    # Body is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    articles.append({"author": author, "pub_date": pub_date, "story": story})
    

logging.info('fetching completed')
fo.write(json.dumps(articles))
fo.close()
cc.close()
c.close()    

