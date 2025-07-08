import feedparser
import requests
import os
import re

# RSS Feed URL
rss_url = "https://www.pjisrael.org/feed/podcast/"

# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Create a folder for downloads
output_dir = "podcast_downloads"
os.makedirs(output_dir, exist_ok=True)

# Download each episode
for entry in feed.entries:
    if 'enclosures' in entry and entry.enclosures:
        mp3_url = entry.enclosures[0].href
        title = entry.title

        # Clean title for filename
        filename = re.sub(r'[\\/*?:"<>|]', "", title)
        filepath = os.path.join(output_dir, f"{filename}.mp3")

        if not os.path.exists(filepath):
            print(f"Downloading: {title}")
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
                response = requests.get(mp3_url, stream=True, headers=headers)
                response.raise_for_status()
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            except Exception as e:
                print(f"Failed to download {title}: {e}")
        else:
            print(f"Already exists: {title}")