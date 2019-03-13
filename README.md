Python script to download all the Luke's English Podcasts from https://teacherluke.co.uk/archive-of-episodes-1-149/.

 The script doesn't download podcast if the file already exists in the directory. So you can stop and resume downloading when needed.

 **Important:** You must have more than 30.3 GB of free space on your drive (HDD, SSD, flash) for all episodes (relevant on moment when #580 is the latest episode) 

**Usage**:

```shell
python3 luke_english_podcast_downloader.py
```
**For Windows users (with only python 3 installed)**:

Copy file "luke_english_podcast_downloader.py" to folder for downloads, then open cmd:
```shell
cd "C:\path\to\downloads"
luke_english_podcast_downloader.py
```

**Prerequisite**:

```shell
pip3 install requests_html
```

**Example of the script execution**:

![Alt text](img/LEP-downloader-screen01.png?raw=true "LEP downloader")

![Alt text](img/LEP-downloader-screen02.png?raw=true "LEP downloader")
