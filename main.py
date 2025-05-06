import os
from pprint import pprint
from youtool import YouTube

api_keys = os.environ.get('API_KEY')
yt = YouTube(api_keys)

url = 'https://www.youtube.com/@kipperdev'

channel_id = yt.channel_id_from_url(url)

maiores_videos = {}

infos_list = []

mini = 0
key = ''

for playlist in yt.channel_playlists(channel_id):
    for video in yt.playlist_videos(playlist['id']):
        for info in yt.videos_infos([video['id']]):
            infos_list.append(info)
for info in infos_list:
    if len(maiores_videos.keys()) == 5:
        menor_valor = 10000000000000000
        menor_obj = ''
        for k,v in maiores_videos.items():
            if v['likes'] < menor_valor:
                menor_valor = v['likes']
                menor_obj = k
        if info['likes'] > menor_valor:
            del maiores_videos[menor_obj]
            maiores_videos[info['id']] = {
                'title': info['title'],
                'likes': info['likes'],
                'comments': info['comments'],
                'views': info['views'],
                'percent_views_like': (int(info['likes']) * 100) / int(info['views']) if info['likes'] and info['views'] else 0
            }
    else:
        maiores_videos[info['id']] = {
            'title': info['title'],
            'likes': info['likes'],
            'comments': info['comments'],
            'views': info['views'],
            'percent_views_like': (int(info['likes']) * 100) / int(info['views']) if info['likes'] and info['views'] else 0
        }

pprint(maiores_videos)
