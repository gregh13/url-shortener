from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4


class Record(BaseModel):
    original_url: str
    custom_url: str | None = None


SHORT_URL_LENGTH = 8

app = FastAPI()


def post_to_db(foo = None, bar = None):
    # placeholder function
    return


@app.get("/")
async def root():
    message = '''
              Welcome to the URL Shortener Application, the free and easy way to shorten long and unseemly URLs. 
              Use a custom short URL or let us randomly generate one.
              '''
    return {"message": message}


@app.post("/shorten_url")
async def shorten_url(record: Record):
    if record.custom_url:
        # Custom url provided, proceed with posting to DB
        db_response = post_to_db(record.custom_url, record.original_url)

    else:
        # No custom url provided, need to generate random short url
        while True:
            random_full_url = uuid4()
            random_short_url = random_full_url
            # random_short_url = str(random_full_url)[:SHORT_URL_LENGTH]
            db_response = post_to_db(random_short_url, record.original_url)
            if not db_response:
                # placeholder if statement
                break

    return db_response
