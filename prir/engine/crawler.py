import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
from pymongo import MongoClient
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

client = MongoClient("mongodb://db:27017/")
db = client["crawler"]
collection = db["data"]

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\+?\d[\d\s\-]{7,}\d"  
ADDRESS_KEYWORDS = ["ul.", "al.", "ulica", "adres", "miejscowość", "kod pocztowy"]
SOCIAL_LINKS_DOMAINS = ["facebook.com", "twitter.com", "linkedin.com", "instagram.com"]

async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            print(f"Pobieranie {url} status: {response.status}")
            return await response.text()
    except Exception as e:
        print(f"Błąd pobierania {url}: {e}")
        return ""

async def process_url(url, profile):
    print(f"Przetwarzam URL: {url} z profilem: {profile}")
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        if not html:
            print(f"Brak danych HTML z {url}")
            return

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        found = set()
        if profile == "emails":
            found = set(re.findall(EMAIL_REGEX, text))
        elif profile == "phones":
            found = set(re.findall(PHONE_REGEX, text))
        elif profile == "addresses":
            for line in text.split("\n"):
                if any(keyword in line.lower() for keyword in ADDRESS_KEYWORDS):
                    found.add(line.strip())
        elif profile == "social_links":
            for a in soup.find_all("a", href=True):
                href = a['href']
                if any(domain in href for domain in SOCIAL_LINKS_DOMAINS):
                    found.add(href)
        else:
            print(f"Profil {profile} nieobsługiwany.")
            return

        if found:
            result = {"url": url, "profile": profile, "data": list(found)}
            collection.insert_one(result)
            print(f"Zapisano {url}: {found}")
        else:
            print(f"Nie znaleziono danych dla profilu {profile} na {url}")

async def crawl_all(urls, profile):
    tasks = [process_url(url, profile) for url in urls]
    await asyncio.gather(*tasks)

def crawl_process(args):
    urls, profile = args
    asyncio.run(crawl_all(urls, profile))

def start_crawling(urls, profile):
    N = min(4, len(urls))
    chunk_size = (len(urls) + N - 1) // N
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    with Pool(processes=N) as pool:
        pool.map(crawl_process, [(chunk, profile) for chunk in chunks])

@app.post("/crawl")
async def crawl(request: Request):
    payload = await request.json()
    urls = payload.get("urls", [])
    profile = payload.get("profile", "")
    await crawl_all(urls, profile)
    return {"status": "ok"}

@app.get("/results")
async def get_results():
    results = []
    cursor = collection.find()
    for doc in cursor:
        results.append({
            "url": doc.get("url", ""),
            "profile": doc.get("profile", ""),
            "data": doc.get("data", [])
        })
    print("Zwracane wyniki:", results)  
    return JSONResponse(content=results)
