import os
import requests
from http.cookiejar import MozillaCookieJar
from bs4 import BeautifulSoup

def load_cookies(file_path):
    cj = MozillaCookieJar()
    cj.load(file_path, ignore_discard=True, ignore_expires=True)
    return cj

cookies = load_cookies("cookies.txt")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

url = "https://www.planetminecraft.com/member/mattbatwings/"

r = requests.get(url, headers=headers, cookies=cookies)

if r.status_code == 200:
    print("[SUCCESS] Page loaded. Here's a preview:")
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.select("a[href]"):
        href = link["href"]
        if any(href.endswith(ext) for ext in [".zip", ".schematic", ".mcworld"]):
            print("Download:", href)
else:
    print(f"[FAIL] Status code: {r.status_code}")
