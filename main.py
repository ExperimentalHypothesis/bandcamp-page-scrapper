import argparse
import subprocess

from src.scrapper import scrape_bandcamp_url


def parse_args():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Scrape all album URLs from a Bandcamp /music page.")
    parser.add_argument("url", help="The full URL of the Bandcamp /music page.")
    # parser.add_argument("base_dir", help="The path where albums will be downloaded.", default=".")
    return parser.parse_args()


def main():
    """
    Main function to handle command-line arguments and print results.
    """
    args = parse_args()
    album_links = scrape_bandcamp_url(args.url)

    if album_links:
        print(f"\nSuccess! Found {len(album_links)} unique album links:")
        for link in sorted(album_links):
            print(f"\n---> Downloading: {link}")
            command_list = ['bandcamp-dl', link]
            try:
                subprocess.run(command_list, check=True)
            except FileNotFoundError:
                print(f"ERROR: The command 'bandcamp-dl' was not found.")
                print("Please make sure bandcamp-dl is installed and in your system's PATH.")
                break  # Stop the script if the command doesn't exist
            except subprocess.CalledProcessError as e:
                print(f"ERROR: bandcamp-dl failed for URL {link} with error: {e}")
    else:
        print("\nProcess finished. No album links were found for the given URL.")

if __name__ == "__main__":
    main()
