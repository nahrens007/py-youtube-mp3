from __future__ import unicode_literals
import youtube_dl

with open('links.txt', 'r') as file:
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '192',
    }],
    }
    for line in file:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([line])
