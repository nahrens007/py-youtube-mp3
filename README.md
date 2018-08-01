# py-youtube-mp3
Download youtube videos specified in links.txt (same directory as where the python script is located). Must have youtube_dl installed. 
## Dependencies
### Python
Regardless of whether you're using Linux or Windows, your Python environment requires the youtube_dl module. 
I installed it by running the command: 
`pip3 install youtube_dl`
### Linux
If you're running Linux, then you will need to install ffmpeg. I installed it by running: 
`sudo apt-get install ffmpeg`
### Windows
Same as with Linux, you need to install ffmpeg. You can download it here: https://www.ffmpeg.org/
## Running
Finally, running: 
`python3 youtube-mp3.py`
will beging the process of downloading and processesing the youtube videos listed in links.txt.
