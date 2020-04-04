from __future__ import unicode_literals
import youtube_dl
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not os.path.isdir(os.path.join(BASE_DIR,'logs')):
    # create logs/ dir
    os.mkdir(os.path.join(BASE_DIR,'logs'))
    
with open(os.path.join(BASE_DIR,'links.txt'), 'r') as file:
    songs = json.loads(file.read())
    now = datetime.now()
    current_time = now.strftime("%Y%m%d%H%M%S")
    log=open(os.path.join(BASE_DIR,'logs','yt_dl_'+current_time+'.log'),'w')
    log.write(json.dumps(songs,sort_keys=True, indent=4, separators=(',',': ')))
    log.close()
    for song in songs:
        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': song['title'] + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': ['-metadata', 'artist='+song['artist'], '-metadata', 'title=' + song['title'], '-metadata', 'album=' + song['album']],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song['url']])


f = open(os.path.join(BASE_DIR,'links.txt'), 'w')
#file format: [{"url":"YoutubeLink","artist":"SongArtist","title":"SongTitle","album":"SongAlbum"}]
f.write('')
f.close()
