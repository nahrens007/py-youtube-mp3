from __future__ import unicode_literals
from yt_dlp import YoutubeDL
import json
import os
import logging, logging.config
import requests


BASE_URL = os.environ.get("BASE_URL")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.isdir(LOG_DIR):
    # create logs/ dir
    os.mkdir(LOG_DIR)


def setup_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {"default": {"format": "[%(levelname)s|%(name)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s", "datefmt": "%Y-%m-%dT%H:%M:%S%z"}},
            "handlers": {
                "file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": os.path.join(LOG_DIR, "yt_dl.log"),
                    "formatter": "default",
                    "when": "midnight",
                    "interval": 1,
                    "backupCount": 30,
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "root": {"level": "INFO", "handlers": ["file", "console"]},
        }
    )


setup_logging()
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger()

logger.info("Starting program")

logger.info(f"{BASE_URL=}")
logger.info(f"{BASE_DIR=}")


def debug_log(func):
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering function: {func.__name__}")
        result = func(*args, **kwargs)
        logger.debug(f"Exiting function: {func.__name__}")
        return result

    return wrapper


@debug_log
def get_music(base_url):
    get_url = f"{base_url}/music"
    logger.info(f"Getting music list from: {get_url=}")

    # Get music from get_url
    response = requests.get(get_url)
    logger.info(f"{response.status_code=}")

    json_data = response.json()
    music_list = json_data.get("music")
    logger.info(f"Retrieved music list with: {len(music_list)=}")
    return music_list


@debug_log
def download_music(music_list):
    
    for song in music_list:
        logger.info(f"Downloading: {song['url']}")
        ydl_opts = {
            "format": "mp3/bestaudio/best",
            "outtmpl": song["title"] + ".%(ext)s",
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "postprocessor_args": ["-metadata", "artist=" + song["artist"], "-metadata", "title=" + song["title"], "-metadata", "album=" + song["album"]],
        }
        with YoutubeDL(ydl_opts) as ydl:
            logger.debug(f"Downloading: {song['title']}")
            status_code = ydl.download([song["url"]])
            logger.info(f"{status_code=}")


if __name__ == "__main__":
    music_list = get_music(BASE_URL)
    download_music(music_list)
