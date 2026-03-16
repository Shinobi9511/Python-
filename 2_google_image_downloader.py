import os
import re
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}


def fetch_image_urls(query: str, count: int) -> list:
    """Scrape image URLs from DuckDuckGo image search."""
    params = urlencode({"q": query, "iax": "images", "ia": "images"})
    url = f"https://duckduckgo.com/?{params}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f" Failed to fetch search page: {e}")
        return []

    vqd_match = re.search(r"vqd='([\d-]+)'", response.text)
    if not vqd_match:
        vqd_match = re.search(r'vqd="([\d-]+)"', response.text)
    if not vqd_match:
        print(" Could not retrieve search token. Try again later.")
        return []

    vqd = vqd_match.group(1)

    image_api = (
        f"https://duckduckgo.com/i.js?l=us-en&o=json&q={query}"
        f"&vqd={vqd}&f=,,,&p=1"
    )

    try:
        api_resp = requests.get(image_api, headers=HEADERS, timeout=10)
        api_resp.raise_for_status()
        data = api_resp.json()
    except Exception as e:
        print(f" Failed to fetch image data: {e}")
        return []

    urls = [result["image"] for result in data.get("results", [])]
    return urls[:count]


def download_images(query: str, count: int, save_folder: str):
    """Download images and save to folder."""
    os.makedirs(save_folder, exist_ok=True)
    print(f"\n Searching for: '{query}'")
    print(f" Saving to: {os.path.abspath(save_folder)}\n")

    urls = fetch_image_urls(query, count)
    if not urls:
        print("  No image URLs found. Check your query or network.")
        return

    downloaded = 0
    for i, url in enumerate(urls, start=1):
        try:
            ext = url.split("?")[0].rsplit(".", 1)[-1]
            if ext.lower() not in ("jpg", "jpeg", "png", "gif", "webp"):
                ext = "jpg"
            filename = os.path.join(save_folder, f"{query.replace(' ', '_')}_{i}.{ext}")
            resp = requests.get(url, headers=HEADERS, timeout=10, stream=True)
            resp.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f" [{i}/{len(urls)}] Saved: {os.path.basename(filename)}")
            downloaded += 1
        except Exception as e:
            print(f" [{i}/{len(urls)}] Failed: {e}")

    print(f"\n Done! {downloaded}/{len(urls)} images downloaded.\n")


def main():
    print("=" * 45)
    print("        GOOGLE IMAGE DOWNLOADER")
    print("=" * 45)

    query = input("\n  Enter search query: ").strip()
    if not query:
        print("  No query entered. Exiting.")
        return

    try:
        count = int(input("  How many images to download? (1-20): ").strip())
        count = max(1, min(count, 20))
    except ValueError:
        print("  Invalid number, defaulting to 5.")
        count = 5

    folder = input(f"  Save folder name [default: '{query}_images']: ").strip()
    if not folder:
        folder = f"{query.replace(' ', '_')}_images"

    download_images(query, count, folder)


if __name__ == "__main__":
    main()
