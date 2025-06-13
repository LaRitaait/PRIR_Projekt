from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re

app = FastAPI()

client = MongoClient("mongodb://db:27017/")
db = client["crawler"]
collection = db["data"]

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\+?\d[\d\s\-]{7,}\d"
ADDRESS_KEYWORDS = ["ul.", "al.", "ulica", "adres", "miejscowość", "kod pocztowy"]
SOCIAL_LINKS_DOMAINS = ["facebook.com", "twitter.com", "linkedin.com", "instagram.com"]

class CrawlRequest(BaseModel):
    urls: List[str]
    profile: str

async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return await response.text()
    except Exception:
        return ""

async def process_url(url, profile):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        if not html:
            return None
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        if profile == "emails":
            found = set(re.findall(EMAIL_REGEX, text))
        elif profile == "phones":
            found = set(re.findall(PHONE_REGEX, text))
        elif profile == "addresses":
            found = set()
            for line in text.split("\n"):
                if any(keyword in line.lower() for keyword in ADDRESS_KEYWORDS):
                    found.add(line.strip())
        elif profile == "social_links":
            found = set()
            for a in soup.find_all("a", href=True):
                href = a['href']
                if any(domain in href for domain in SOCIAL_LINKS_DOMAINS):
                    found.add(href)
        else:
            return None

        if found:
            return {"url": url, "profile": profile, "data": list(found)}
        else:
            return {"url": url, "profile": profile, "data": []}

@app.post("/crawl")
async def crawl(request: CrawlRequest):
    results = await asyncio.gather(*(process_url(url, request.profile) for url in request.urls))
    saved_results = []
    for res in results:
        if res is not None:
            collection.insert_one(res)
            saved_results.append(res)
    return {"saved": len(saved_results)}

@app.get("/results")
def get_results():
    results = list(collection.find({}, {"_id": 0}))
    return results
