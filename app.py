import requests
import pprint
import subprocess

from bs4 import BeautifulSoup
from BandcampPageParser import BandcampPageParser

parser = BandcampPageParser("https://archivesdubmusic.bandcamp.com")
baseDir = r"C:\Users\lukas.kotatko\Music\bc"

for album in parser.albumUrls:
    subprocess.run(f"bandcamp-dl {album} --base-dir={baseDir}")