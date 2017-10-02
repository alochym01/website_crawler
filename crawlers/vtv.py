# -*- coding: utf-8 -*-
# import MySQLdb
from bs4 import BeautifulSoup, NavigableString
import requests
import re
import datetime

url_test = 'http://127.0.0.1:5000/vtvs/test'
url_create = 'http://127.0.0.1:5000/vtvs/create'


def mysoup(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, "html5lib")
    return soup


soup1 = mysoup("http://vtv.vn/timeline/trang-1.htm")
for li in soup1.findAll('a'):
    try:
        temp_link = 'http://vtv.vn%s' % li.get('href')
        rv = requests.post(url_test, json={'link': temp_link}).text
        if int(rv):
            soup = mysoup(temp_link)
            title = re.sub('\|(.*)$|"', '', soup.title.text)
            source = 'vtv'
            category = temp_link.split('/')[3]
            desc = re.sub('VTV.vn - |"|VTV.vn', '', soup.h2.text)
            pattern_film = re.compile('=vtv/(.*).mp4')
            link_mp4 = 'http://hls.vcmedia.vn/%s' % re.search(
                pattern_film, str(soup)).group().replace('=vtv', 'vtv')
            tags = []
            for tag in soup.find_all("a", {'itemprop': 'keywords'}):
                tags.append(tag.get('title'))
            tags = ','.join(tags)
            data = {
                'title': title,
                'link': temp_link,
                'category': category,
                'description': desc,
                'link_mp4': link_mp4,
                'tags': tags
            }
            requests.post(url_create, json=data)
    except Exception as e:
        print(str(e))
        pass
