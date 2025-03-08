# py-youtube-mp3
Download youtube videos specified in links.txt (same directory as where the python script is located). Must have youtube_dl installed. 
## Dependencies
### Python
Regardless of whether you're using Linux or Windows, your Python environment requires the youtube_dl module. 
    pipenv install
### Linux
If you're running Linux, then you will need to install ffmpeg. I installed it by running: <br/>
    sudo apt-get install ffmpeg
### Windows
Same as with Linux, you need to install ffmpeg. You can download it here: https://www.ffmpeg.org/ <br/>
I downloaded the static-linked zip file, put it in `C:\Program Files\ffmpeg`, and added the path `C:\Program Files\ffmpeg\bin` to my PATH environment variable (ffmpeg.exe, ffplay.exe, and ffprobe.exe are in the bin folder). If you don't know how to add items to the PATH environment variable, you can Google it. Keep in mind you may need to sign out and sign back in for the environment variable to take effect. 
## Running
Finally, running:
    python3 youtube-mp3.py
will beging the process of downloading and processesing the youtube videos listed in links.txt.
