from __future__ import unicode_literals 
import youtube_dl 
import json 
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

try:
    with open(os.path.join(BASE_DIR,'links.txt'), 'r') as file:
        songs = json.load(file)
        for song in  songs:
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
    os.remove(os.path.join(BASE_DIR, 'links.txt'))
except FileNotFoundError:
    print("file doesn't exist...")

