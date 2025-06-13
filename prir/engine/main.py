from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from crawler import start_crawling
from pymongo import MongoClient
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://db:27017/")
db = client["crawler"]
collection = db["data"]

@app.post("/crawl")
async def crawl(request: Request):
    data = await request.json()
    urls = data["urls"]
    profile = data["profile"]
    start_crawling(urls, profile)
    return {"status": "started"}

@app.get("/results")
async def get_results():
    results = list(collection.find({}, {"_id": 0})) 
    return JSONResponse(content=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
