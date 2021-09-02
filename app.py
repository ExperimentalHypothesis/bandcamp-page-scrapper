import requests
import pprint
import subprocess

from bs4 import BeautifulSoup
from BandcampPageParser import BandcampPageParser

parser = BandcampPageParser("https://eileanrec.bandcamp.com/music")
baseDir = r"C:\Users\lukas.kotatko\Music"

for album in parser.albumUrls:
    print(baseDir)
    command = f'bandcamp-dl {album} --base-dir="{baseDir}"'
    print(command)
    subprocess.run(command)