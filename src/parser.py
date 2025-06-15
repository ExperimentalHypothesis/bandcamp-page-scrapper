from urllib.parse import urljoin

from bs4 import BeautifulSoup


class BandcampPageParser:
    """
    Parses a given HTML string to extract all album URLs.
    """
    ALBUM_LOCATOR = "li.music-grid-item a"

    def __init__(self, page_html: str, page_url: str):
        self.soup = BeautifulSoup(page_html, "html.parser")
        self.base_url = page_url

    def get_album_urls(self) -> list:
        """Finds all unique album URLs in the parsed HTML."""
        link_tags = self.soup.select(self.ALBUM_LOCATOR)
        urls = set()
        for link in link_tags:
            href = link.get('href')
            if href:
                full_url = urljoin(self.base_url, href)
                urls.add(full_url)
        return list(urls)


