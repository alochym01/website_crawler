# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from random import randint
from datetime import datetime
import os
import shlex
import re
import requests
import mysql.connector
import wget
from bs4 import BeautifulSoup

python_cmd = '/home/hadn/python3/bin/python'
ffmpeg_cmd = '/usr/bin/ffmpeg'
folder_path = '/mnt/website/v1/vtv_crawler'
folder_download = '/mnt/website/v1/laravel'
water_mark_file = '/mnt/website/v1/vtv_crawler/output_120.png'


def add_to_playlist(videoId):
    cmd = '%s %s/playlist_item_xyz.py --videoId %s' % (
        python_cmd, folder_path, videoId)
    cmd = shlex.split(cmd)
    print(cmd)
    try:
        upload = Popen(cmd, stdout=PIPE)
        upload.communicate()
    except Exception as e:
        print(str(e))


def upload_youtube(link, title, desc, keyword):
    os.chdir(folder_download)
    wget.download(link)
    file_mp4 = link.split("/")[-1]
    temp_file = '%s/%s.mp4' % (folder_download, randint(1, 10000000000000))
    ffmpeg = '%s -i %s -i %s -filter_complex "overlay=main_w-overlay_w-80:100"\
                %s' % (ffmpeg_cmd, file_mp4, water_mark_file, temp_file)
    ffmpeg = shlex.split(ffmpeg)
    print(ffmpeg)
    ffmpeg_up = Popen(ffmpeg, stdout=PIPE)
    ffmpeg_up.communicate()

    cmd = '%s %s/upload_youtube_xyz.py --file "%s" --title "%s" --description "%s"\
            --keywords "%s" --category=25' % (python_cmd, folder_path, temp_file,
                                              title, desc, keyword)
    cmd = shlex.split(cmd)
    print(cmd)
    try:
        upload = Popen(cmd, stdout=PIPE)
        temp = upload.communicate()
        #: remove file which uploaded to youtube
        os.remove(temp_file)
        #: remove file which uploaded to youtube
        os.remove(file_mp4)
        return temp[0].decode('utf-8').strip().split("'")[1]
    except Exception as e:
        print(str(e))
        pass


def getValid(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html5lib")
    temp_time = soup.find('meta', {"name": "pubdate"}).get('content')
    temp_time = re.search(r'\d+-\d+-\d+', temp_time).group()
    if temp_time == datetime.now().strftime('%Y-%m-%d'):
        return True
    return False


db = mysql.connector.connect(user='hadn', password='Hanguyen@123',
                             host='127.0.0.1', database='vtv', use_unicode=True)
cursor = db.cursor()

sql = "select link_mp4, yt_id, id, title, description, link, tags\
        from vtv where category_id='trong-nuoc' and yt_id is NULL limit 1"
cursor.execute(sql)

for (link_mp4, yt_id, id, title, description, link, tags) in cursor:
    if getValid(link):
        url = 'http://vtv.phimabc.xyz/posts/%s/%s/yt_update' % (
            id, 'Uploading')
        requests.get(url)
        try:
            desc = title + description
            print(desc)
            videoId = upload_youtube(link_mp4, title, desc, tags)
            # videoId = upload_youtube(link_mp4,title,desc,'trong-nuoc')
            url = 'http://vtv.phimabc.xyz/posts/%s/%s/yt_update' % (
                id, videoId)
            requests.get(url)
            add_to_playlist(videoId)
        except Exception as e:
            print(str(e))
    else:
        url = 'http://vtv.phimabc.xyz/posts/%s/%s/yt_update' % (id, 'videoId')
        requests.get(url)

cursor.close()
db.close()
