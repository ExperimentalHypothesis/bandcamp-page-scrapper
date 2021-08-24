import requests
from bs4 import BeautifulSoup

class BandcampPageParser:
    ALBUM_LOCATOR = "ol li.music-grid-item"
    LINK_LOCATOR = "a"

    def __init__(self, pageUrl: str):
        page = requests.get(pageUrl).content
        self.soup = BeautifulSoup(page, "html.parser")
        self.pageUrl = pageUrl

    @property
    def albumUrls(self) -> list:
        """ Given a Bandcamp URL page, it returns all downloadable links. """
        return [self._getAlbumUrl(e) for e in self.soup.select(self.ALBUM_LOCATOR)]  
        
    def _getAlbumUrl(self, parrent: str) -> str:
        """ Helper function that parses one album and returns its link. """
        if self.pageUrl.endswith("/music"):
            self.pageUrl = self.pageUrl[:-6]
        return self.pageUrl + parrent.select_one(self.LINK_LOCATOR).attrs["href"]
