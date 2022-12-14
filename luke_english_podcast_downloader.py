#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download all Luke’s ENGLISH Podcast files(only mp3 files) listed in https://teacherluke.co.uk/archive-of-episodes-1-149/.
You don't need to open every link and right click to download Podcastself.
'python3 luke_english_podcast_downloader.py' will do the job for you.

Author: Pavan J
"""
"""
Updating by 'hotenov':
(2019-03-13)
- excluding illegal characters from filename (via regex thanks to 'Enigma' http://network.ubotstudio.com/forum/index.php/topic/17406-tutorial-regex-illegal-characters-in-path/#entry105434 )
- exception handling (thanks to 'XavierCLL' and 'Arpad Horvath' https://stackoverflow.com/a/36896675/3366563 and 'ProfHase85' https://stackoverflow.com/a/21407552/3366563)
- displaying of current processing link (file) with colorized status (thanks to 'rabin utam' https://stackoverflow.com/a/21786287/3366563)
- downloading all mp3 files on the page (for multipart episodes and links to other materials)
"""

from requests_html import HTMLSession
from urllib import request
import os
import re
from urllib import error
from requests.exceptions import ConnectionError

# COUNTERS #
on_disc = 0
downloaded = 0
mp3_broken = 0
page_not_found = 0
no_audio = 0
all_posts = 0

# Start session
session = HTMLSession()
r = session.get('https://teacherluke.co.uk/archive-of-episodes-1-149/')

# Find all links in 'entry-content' class, containing in 'href' attribute with "https://teacherluke.co.uk" or "wp.me" strings
all_links = r.html.find('.entry-content a[href*="https://teacherluke.co.uk"], .entry-content a[href*="wp.me"]')

for link in reversed(all_links):  # Reversed for processing from 1: latest on site - latest on disc
    all_posts += 1
    # Replace illegal characters
    target_file = re.sub('[@,\"^:;*|\\/?><=\\\\/]', '_', link.text) + '.mp3'
    # If episode is already downloaded 
    if os.path.exists(target_file):
        print("file: {title} \x1b[0;30;47m{status}\x1b[0m".format(title=link.full_text, link=link.attrs['href'], status="ON DISC"))
        on_disc += 1
        # go to next link
        continue 
    try:
        # Check in try block that link is available, with redirects (for several wp.me links)
        resp = session.head(link.attrs['href'], allow_redirects=True)
    except ConnectionError as e:
        print("file: {title}  \x1b[1;30;41m{status}\x1b[0m [{link}]".format(title=link.full_text, link=link.attrs['href'], status="PAGE NOT FOUND"))
        resp = "No response"
        page_not_found +=1
    except error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        print('HTTPError: {code} LINK={link}'.format(code = e.code, link = link.attrs['href']))
        page_not_found +=1
    except error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        print('URLError: {}'.format(e.reason))
        page_not_found +=1
    else:
        # 200
        print("file: {title} ".format(title=link.full_text, link=link.attrs['href']), end='')
        sub_r = session.get(resp.url)
        # Find all links with key words in 'entry-content' class
        download_link_a = sub_r.html.find('.entry-content a', containing=['DOWNLOAD', 'Download', 'Right-click'])
        # Calulate the number of links
        all_downloaded_links = len(download_link_a)
        # If there is one or more
        if all_downloaded_links > 0:
            part = 1
            for part_link in reversed(download_link_a):
                # Take only links to mp3 files 
                if part_link and '.mp3' in part_link.attrs['href']:
                    mp3_link = part_link.attrs['href']
                    try:
                        open_mp3 = request.urlopen(mp3_link)
                    except error.HTTPError as e:
                        # Return code error (e.g. 404, 501, ...)
                        print('\x1b[0;30;41m{status}\x1b[0m Details: {code} [{link_to_file}]'.format(code=e.code,link_to_file=mp3_link,status="MP3 FILE BROKEN"))
                        mp3_broken += 1
                        continue
                    except error.URLError as e:
                        # Not a HTTP-specific error (e.g. connection refused)
                        print('URLError: {}'.format(e.reason))
                        mp3_broken += 1
                        continue
                    else:
                        # 200
                        mp3_data = open_mp3.read()
                        # if there is only one download link
                        if part < 2:
                            # Write file on disc
                            with open(target_file, 'wb') as audio:
                                audio.write(mp3_data)
                            print("\x1b[1;37;42m{status}\x1b[0m".format(status="DOWNLOADED"))
                            downloaded += 1
                            part += 1
                        # If there are another parts of episode or links to other mp3 materials. In this case add '[Part X]' to the end of file
                        else:
                            target_file = re.sub('[@,\"^:;*|\\/?><=\\\\/]', '_', link.text) + ' [Part ' + str(part) +  ']' + '.mp3'
                            with open(target_file, 'wb') as audio:
                                audio.write(mp3_data)
                            print("file: {title} [Part {part}] \x1b[1;37;42m{status}\x1b[0m".format(status="DOWNLOADED", part=part, title=link.full_text))
                            downloaded += 1
                            part += 1
                # If NO mp3 dowloads
                else:
                    if part < 2:
                        print("\x1b[5;30;43m{status}\x1b[0m ".format(status="NO AUDIO"))
                        no_audio += 1
                    else:
                        print("file: {title} [Part {part}] \x1b[1;37;42m{status}\x1b[0m".format(status="NO AUDIO", part=part, title=link.full_text))
                        no_audio += 1
        # If NO downloads links at all
        else:
            print("\x1b[5;30;43m{status}\x1b[0m".format(status="NO AUDIO"))
            no_audio += 1
                
info_text = """
\x1b[0;35;40mSome episodes are not available by links (but you can listen to it in player on the website). Here they are:\x1b[0m
83. How to Swear in British English – VERY RUDE CONTENT (with James) -> \x1b[0;36;40mhttps://teacherluke.co.uk/2012/01/30/how-to-swear-in-british-english-very-rude-content/\x1b[0m
128. Luke’s Stand-Up Comedy Show -> \x1b[0;36;40mhttps://teacherluke.co.uk/2013/04/07/795/\x1b[0m
Luke’s Interview on InglesPodcast -> \x1b[0;36;40mhttp://www.inglespodcast.com/2015/03/31/mansion-interviews-luke-thompson-from-lukes-english-podcast/\x1b[0m
579. [2/2] IELTS Q&A with Ben Worthington from IELTS Podcast -> \x1b[0;36;40mhttps://teacherluke.co.uk/2019/03/01/579-2-2-ielts-qa-with-ben-worthington-from-ielts-podcast/\x1b[0m 

\x1b[0;35;40mAnd one wrong link (typo):\x1b[0m
London Olympics 2012 -> \x1b[0;36;40mhttps://teacherluke.co.uk/2012/08/06/london-olympics-2012/\x1b[0m 
\x1b[0;35;40mRelevant: 13 March 2019\x1b[0m
"""


# display summary        
print("--------------------")
print("ALL Links - {counter}".format(counter=all_posts))
print("\x1b[1;37;42m{status}\x1b[0m - {counter}".format(status="DOWNLOADED", counter=downloaded))
print("\x1b[0;30;47m{status}\x1b[0m - {counter}".format(status="ON DISC", counter=on_disc))
print("\x1b[5;30;43m{status}\x1b[0m - {counter}".format(status="NO AUDIO", counter=no_audio))
print("\x1b[0;30;41m{status}\x1b[0m - {counter}".format(status="MP3 FILE BROKEN", counter=mp3_broken))
print("\x1b[1;30;41m{status}\x1b[0m - {counter}".format(status="PAGE NOT FOUND", counter=page_not_found))    
print("--------------------")
print(info_text)
print("\x1b[0;32;40mDone!\x1b[0m")
