import json
from typing import List
from fastapi import FastAPI
import uvicorn
from crawler.crawler import Crawler

app = FastAPI()


@app.get('/status')
async def main():
    return {'status': 'ok'}


# localhost:8000/smartphones?price=329900
@app.get('/smartphones/{price}', response_model=)
