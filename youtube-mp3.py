from __future__ import unicode_literals
import youtube_dl
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR,'links.txt'), 'r') as file:
    for line in file:
        if line.startswith("#"):
            continue
        song = json.loads(line)
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
#f.write('#{"url":"YoutubeLink","artist":"SongArtist","title":"SongTitle","album":"SongAlbum"}') # empty the file
f.write('')
f.close()
