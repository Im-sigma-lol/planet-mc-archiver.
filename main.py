import os
import re
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.planetminecraft.com"

def get_user_projects(username):
    page = 1
    project_urls = []

    while True:
        url = f"{BASE_URL}/member/{username}/?p={page}"
        print(f"[INFO] Checking: {url}")
        r = requests.get(url)
        if r.status_code != 200:
            print(f"[ERROR] Unable to access page: {url}")
            break

        soup = BeautifulSoup(r.text, 'html.parser')
        projects = soup.select("a.stretched-link")
        if not projects:
            break

        for link in projects:
            href = link.get("href")
            if href and href.startswith("/project/"):
                full_url = urljoin(BASE_URL, href)
                project_urls.append(full_url)

        page += 1

    return project_urls

def download_project_file(project_url, user_folder):
    r = requests.get(project_url)
    soup = BeautifulSoup(r.text, "html.parser")
    download_link = soup.find("a", string=re.compile(r"Download.*", re.IGNORECASE))

    if download_link:
        file_url = urljoin(BASE_URL, download_link.get("href"))
        file_name = file_url.split("/")[-1].split("?")[0]
        dest_path = os.path.join(user_folder, file_name)

        if os.path.exists(dest_path):
            print(f"[SKIP] Already downloaded: {file_name}")
            return

        print(f"[DOWNLOAD] {file_name} from {file_url}")
        with requests.get(file_url, stream=True) as rfile:
            rfile.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in rfile.iter_content(chunk_size=8192):
                    f.write(chunk)
    else:
        print(f"[WARNING] No download link found on: {project_url}")

def main():
    parser = argparse.ArgumentParser(description="Download all Planet Minecraft files from a user.")
    parser.add_argument('-u', '--user', required=True, help='Planet Minecraft username')
    args = parser.parse_args()

    username = args.user
    user_folder = os.path.join(os.getcwd(), username)

    os.makedirs(user_folder, exist_ok=True)
    projects = get_user_projects(username)

    print(f"[INFO] Found {len(projects)} projects for user '{username}'")

    for url in projects:
        try:
            download_project_file(url, user_folder)
        except Exception as e:
            print(f"[ERROR] Failed to download from {url}: {e}")

if __name__ == "__main__":
    main()
