import requests
import yt_dlp
import json
import os
from True_Tiktok_Uploader.upload import upload_video
from TrueGIXERJ_Utils.files import sanitise
from TrueGIXERJ_Utils.logger import logger
import config
from datetime import datetime, timedelta

def load_used_videos():
    """
    Loads the list of previously used video URLs from the storage file defined in config.

    :return: a list of video URLs
    """
    if os.path.exists(config.STORAGE_FILE):
        logger.info("Loading used videos...")
        with open(config.STORAGE_FILE, "r") as f:
            try:
                used_videos = json.load(f)
            except json.JSONDecodeError:
                return []
        cutoff_time = datetime.now() - timedelta(days=7)
        logger.info(f"Pruning old entries in {config.STORAGE_FILE}")
        used_videos = {
            url: timestamp for url, timestamp in used_videos.items()
            if datetime.fromisoformat(timestamp) > cutoff_time
        }
        return used_videos
    else:
        return []
    
def save_used_videos(used_videos):
    """
    Saves the list of used video URLs to the storage file defined in config.

    :param used_videos: a list of video URLs which have been used
    """
    logger.info(f"Saving video to {config.STORAGE_FILE}")
    with open(config.STORAGE_FILE, "w") as f:
        json.dump(used_videos, f, indent=4)

def get_top_video(used_videos):
    """
    Fetches the top video from the subreddit defined in config, that has not been used before

    :param used_videos: a list of video URLs which have been used
    :return: a dictionary containing post data, or None if there is no new videos found
    """
    try:
        response = requests.get(config.SUBREDDIT_URL, headers={"User-Agent": "Mozilla/5.0"})
    except Exception as e:
        logger.error("Couldn't reach Reddit.")
        logger.error(e)
        return None
    if response.status_code != 200:
        logger.error("Failed to fetch subreddit data.")
        return None
    
    data = response.json()
    for post in data['data']['children']:
        post_data = post['data']
        if post_data['is_video'] and post_data['url'] not in used_videos:
            return post_data
    return None

def download_video(url, output_path):
    """
    Downloads a video from the given URL using yt_dlp and saves it to the specified output path

    :param url: the URL of the video to download
    :output_path: the path to save the downloaded file
    """
    ydl_opts = {
        "outtmpl": output_path,
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    """
    Main function.
    Finds a new video, downloads it, uploads to tiktok, and then logs the used video.
    """
    used_videos = load_used_videos()
    post_data = get_top_video(used_videos)
    
    if not post_data:
        logger.error("No new videos found.")
        return

    title, author, url = post_data['title'], post_data['author'], post_data['url']
    logger.info(f"Downloading: {title} by {author}")
    safe_title = sanitise(title)[:100]
    video_path = f'{safe_title}.mp4'

    download_video(url, video_path)

    description = f"{safe_title} - u/{author} - {config.HASHTAGS}"
    upload_video(video_path, description, 'cookies.txt', True)
    
    used_videos[url] = datetime.now().isoformat()
    save_used_videos(used_videos)

    os.remove(video_path)
    logger.success('File Deleted.')

if __name__ == "__main__":
    main()
