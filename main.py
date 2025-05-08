import os
from dotenv import load_dotenv
from pymongo import MongoClient
from youtool import YouTube
from pprint import pprint

load_dotenv()
api_keys = os.environ.get('API_KEY')
mongo_uri = os.environ.get('MONGO_URI')

yt = YouTube([api_keys])
client = MongoClient(mongo_uri)
db = client['youtube_db']
collection = db['video']

# collection.drop()

url = 'https://www.youtube.com/@kipperdev'
channel_id = yt.channel_id_from_url(url)

infos_list = []

for playlist in yt.channel_playlists(channel_id):
    for video in yt.playlist_videos(playlist['id']):
        for info in yt.videos_infos([video['id']]):
            infos_list.append(info)
if infos_list:
    collection.insert_many(infos_list)

top_videos = collection.aggregate([
    {
        '$group': {
            '_id': '$title',
            'title': {'$first': '$title'},
            'likes': {'$first': '$likes'},
            'comments': {'$first': '$comments'},
            'views': {'$first': '$views'}
        }
    },
    {
        '$sort': {'likes': -1}
    },
    {
        '$limit': 5
    }
])

pprint(list(top_videos))
