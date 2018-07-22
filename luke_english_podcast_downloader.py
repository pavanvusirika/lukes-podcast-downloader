#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download all Luke’s ENGLISH Podcast files(only mp3 files) listed in https://teacherluke.co.uk/archive-of-episodes-1-149/.
You don't need to open every link and right click to download Podcastself.
'python3 luke_english_podcast_downloader.py' will do the job for you.

Author: Pavan J
"""

from requests_html import HTMLSession
from urllib import request
import os

session = HTMLSession()
r = session.get('https://teacherluke.co.uk/archive-of-episodes-1-149/')
all_links = r.html.find("div.entry-content a")
for link in all_links:
    target_file = "{}.mp3".format(link.text.replace(r"/", "_"))
    if os.path.exists(target_file):
        continue
    if 'teacherluke.co.uk' in link.attrs['href']:
        sub_r = session.get(link.attrs['href'])
        download_link_a = sub_r.html.find('a',containing=['DOWNLOAD', 'Download', 'Right-click'], first=True)
        if download_link_a and 'teacherluke' in download_link_a.attrs['href'] and '.mp3' in download_link_a.attrs['href']:
            mp3_link = download_link_a.attrs['href']
            open_mp3 = request.urlopen(mp3_link)
            mp3_data = open_mp3.read()
            #with open(mp3_link.split("/")[-1], 'wb') as audio:
            with open(target_file, 'wb') as audio:
                audio.write(mp3_data)
print("Done!")
