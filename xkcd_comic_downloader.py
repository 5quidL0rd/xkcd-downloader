import os
import time
import requests

# Directory to save the XKCD comics
SAVE_DIR = "xkcd_comics"
INTERVAL = 3600  # Time interval to check for new comic (in seconds)

def get_latest_comic():
    """Fetch the latest XKCD comic info."""
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch the latest XKCD comic.")
        return None

def download_comic(comic):
    """Download the given comic."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    img_url = comic['img']
    title = comic['title']
    number = comic['num']

    # Get the image filename from the URL
    img_name = f"xkcd_{number}_{title.replace(' ', '_')}.png"
    img_path = os.path.join(SAVE_DIR, img_name)

    # Download the image
    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        with open(img_path, 'wb') as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)
        print(f"Downloaded comic #{number}: {title}")
    else:
        print(f"Failed to download comic #{number}: {title}")

def main():
    last_comic_number = None

    while True:
        try:
            latest_comic = get_latest_comic()
            if latest_comic:
                current_comic_number = latest_comic['num']

                # Check if the comic is new
                if last_comic_number != current_comic_number:
                    download_comic(latest_comic)
                    last_comic_number = current_comic_number
                else:
                    print("No new comic available yet.")

        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait before checking again
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
