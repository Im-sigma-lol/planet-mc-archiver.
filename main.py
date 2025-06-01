import requests
from bs4 import BeautifulSoup

USERNAME = "mattbatwings"  # change with -u flag in final version
PHPSESSID = ""  # paste your cookie value here

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
session.cookies.set("PHPSESSID", PHPSESSID, domain="planetminecraft.com")

url = f"https://www.planetminecraft.com/member/{USERNAME}/?p=1"
response = session.get(url)

if response.status_code == 200:
    print("[SUCCESS] Loaded page")
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract project links
    projects = soup.select("a.stretched-link")
    for a in projects:
        title = a.get("title")
        href = a.get("href")
        print("Project:", title, "->", f"https://www.planetminecraft.com{href}")
else:
    print(f"[ERROR] Status code {response.status_code}")
