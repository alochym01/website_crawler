from random import randint
import feedparser
import requests

url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCP0bPNhoWonVH_6NI4ZBGNw"

data = feedparser.parse(url)

feeds = []
for entry in data.entries:
    temp = {}
    temp = {
        "author": entry.author,
        "published": entry.published,
        "description": entry.title,
        "title": entry.title,
        "yt_videoid": entry.yt_videoid
    }
    print(entry.yt_videoid)
    # ready to insert data into database
    rv = requests.post('http://127.0.0.1:5000/video/create', json=temp)
    feeds.append(temp)
