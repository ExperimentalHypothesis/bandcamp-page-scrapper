import requests
import pprint
import subprocess

from bs4 import BeautifulSoup
from BandcampPageParser import BandcampPageParser

parser = BandcampPageParser("https://voiceofeye.bandcamp.com/")
baseDir = "C:\\Users\\lukas.kotatko\\Music\\VoiceOfEye"

for album in parser.albumUrls:
    print(baseDir)
    subprocess.run(f"bandcamp-dl {album} --base-dir={baseDir}")