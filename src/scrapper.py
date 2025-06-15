import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from src.parser import BandcampPageParser


def get_full_page_html(url: str) -> str:
    """
    Uses Selenium to load a page, scroll to the very bottom to trigger all
    dynamic content, and then returns the final, complete HTML.
    """
    print("Setting up browser...")
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in the background
    chrome_options.add_argument("--log-level=3")  # Suppress console noise

    # webdriver-manager will automatically download and manage the driver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f"Navigating to {url}...")
    driver.get(url)

    # --- Scrolling Logic ---
    print("Page loaded. Scrolling to reveal all albums...")
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new content to load.
        time.sleep(2)  # Adjust sleep time if connection is slow

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the page.")
            break
        last_height = new_height

    # Get the final page source after all dynamic content has loaded
    full_html = driver.page_source
    driver.quit()

    return full_html

def scrape_bandcamp_url(url: str) -> List[str]:
    """
    Orchestrates the scraping process for a single Bandcamp URL.
    """
    complete_html = get_full_page_html(url)

    if not complete_html:
        print("Could not retrieve page HTML. Returning empty list.")
        return []

    print("\nParsing the complete HTML...")
    return BandcampPageParser(page_html=complete_html, page_url=url).get_album_urls()
