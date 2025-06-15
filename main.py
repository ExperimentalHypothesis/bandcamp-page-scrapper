import argparse
import asyncio

from src.scrapper import scrape_bandcamp_url


def parse_args():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Scrape all album URLs from a Bandcamp /music page.")
    parser.add_argument("url", help="The full URL of the Bandcamp /music page.")
    parser.add_argument(
        "-c", "--concurrency",
        type=int,
        default=5,
        help="The number of albums to download at the same time. Default is 5."
    )
    return parser.parse_args()

# A function to check disk space (simulated)
async def check_disk_space(event: asyncio.Event):
    print("Running pre-flight check: checking disk space...")
    await asyncio.sleep(5) # Simulate a slow check
    print("Disk space check complete.")
    free_space_ok = True # Assume it's okay
    if free_space_ok:
        print("Pre-flight check passed. Allowing downloads to start.")
        event.set()


async def write_log(message: str, lock: asyncio.Lock):
    async with lock:
        with open("activity.log", "a") as f:
            f.write(f"{message}\n")

async def download_album(link: str, semaphore: asyncio.Semaphore, lock: asyncio.Lock, event: asyncio.Event):
    """
    Asynchronously downloads a single album, respecting the semaphore to limit concurrency.
    """
    await event.wait()
    async with semaphore:
        await write_log(f"Starting download: {link}", lock)
        command_list = ['bandcamp-dl', link]

        process = await asyncio.create_subprocess_exec(
            *command_list,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            await write_log(f"Finished download: {link}", lock)
        else:
            print(f"ERROR downloading {link}. Return code: {process.returncode}")
            if stderr:
                print(f"Details: {stderr.decode().strip()}")


async def main():
    """
    Main asynchronous function to handle argument parsing and orchestrate concurrent downloads.
    """
    args = parse_args()
    album_links = scrape_bandcamp_url(args.url)
    if not album_links:
        print("\nProcess finished. No album links were found for the given URL.")

    print(f"\nSuccess! Found {len(album_links)} unique album links.")
    downloads_allowed_event = asyncio.Event()
    print(f"Starting concurrent downloads (up to {args.concurrency} at a time)...\n")

    semaphore = asyncio.Semaphore(args.concurrency)
    log_lock = asyncio.Lock()

    tasks = [download_album(link, semaphore, log_lock, downloads_allowed_event) for link in sorted(album_links)]
    await asyncio.gather(check_disk_space(downloads_allowed_event), *tasks)

    print("\nAll downloads have completed.")



if __name__ == "__main__":
    asyncio.run(main())
