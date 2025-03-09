from __future__ import unicode_literals
from yt_dlp import YoutubeDL
import os
import requests
from dataclasses import dataclass, fields
from mylogger import setup_logging
import logging
import datetime
import json

# Set up logging at module level
setup_logging(os.path.join(os.environ.get("LOG_DIR", "."), "yt_dl.log"))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class Paths:
    BASE_URL: str
    MUSIC_DIR: str
    HISTORY_DIR: str

    @classmethod
    def from_env(cls) -> "Paths":
        # Get all field names from the dataclass
        env_values = {field.name: os.environ.get(field.name) for field in fields(cls)}
        return cls(**env_values)

    def validate(self) -> bool:
        """Validate that all required paths are set"""
        return all(getattr(self, field.name) for field in fields(self))

    def ensure_directories(self) -> None:
        """Create directories if they don't exist"""
        dir_fields = [field.name for field in fields(Paths) if "dir" in field.name.lower()]
        for dir_name in dir_fields:
            path = getattr(self, dir_name)
            if path and not os.path.isdir(path):
                os.makedirs(path, exist_ok=True)


def debug_log(func):
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering function: {func.__name__}")
        result = func(*args, **kwargs)
        logger.debug(f"Exiting function: {func.__name__}")
        return result

    return wrapper


@debug_log
def get_music_list(base_url):
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
def delete_music(base_url, music_id_list):
    del_url = f"{base_url}/music"
    logger.info(f"Deleting music from: {del_url=}")
    logger.debug(f"{music_id_list=}")
    try:
        response = requests.delete(del_url, json={"delete_list": music_id_list})
        logger.info(f"{response.status_code=}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting music", exc_info=True)
        return None


@debug_log
def download_music(music_list, save_dir):
    success_id_list, fail_id_list = [], []
    for song in music_list:
        logger.info(f"Downloading: {song['title']}")
        ydl_opts = {
            "format": "mp3/bestaudio/best",
            "paths": {"home": save_dir},
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
        try:
            with YoutubeDL(ydl_opts) as ydl:
                logger.debug(f"Downloading: {song['url']}")
                status_code = ydl.download([song["url"]])
        except Exception as e:
            logger.error(f"Error downloading {song['title']}", exc_info=True)
            fail_id_list.append(song["id"])
        finally:
            logger.info(f"{status_code=}")
            if status_code == 0:
                success_id_list.append(song["id"])
            else:
                fail_id_list.append(song["id"])
    return success_id_list, fail_id_list


def main():
    paths = Paths.from_env()
    if not paths.validate():
        logger.error("Missing required environment variables")
        exit(1)
    paths.ensure_directories()

    music_list = get_music_list(paths.BASE_URL)

    # Write music_list to history_dir with timestamp filename following ISO standards
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    history_file = os.path.join(paths.HISTORY_DIR, f"{timestamp_str}.json")
    with open(history_file, "w") as f:
        f.write(json.dumps({"music": music_list}, indent=4))

    success_id_list, fail_id_list = download_music(music_list, paths.MUSIC_DIR)
    logger.info(f"Downloaded: {len(success_id_list)=}")
    logger.info(f"Failed: {len(fail_id_list)=}")

    delete_music(paths.BASE_URL, fail_id_list)


if __name__ == "__main__":
    main()
