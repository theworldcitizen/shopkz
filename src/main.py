from typing import List

from fastapi import FastAPI
import uvicorn
from crawler.readfile import Readfile
from models import Ad

app = FastAPI()


@app.get('/status')
async def main():
    return {'status': 'ok'}


@app.get('/smartphones/{price}', response_model=List[Ad])
async def get_data(price):
    obj = Readfile()
    result = obj.read_file()
    answer = []

    for x in result:
        try:
            a = x.get('price').split()
            new_price = ''
            del a[-1]
            for el in a:
                new_price += el
            if new_price == price:
                answer.append(x)
        except Exception:
            continue

    return answer


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)