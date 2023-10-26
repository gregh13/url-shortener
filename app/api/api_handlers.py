from app.models.pydantic_models import PostURL, GetURL
from app.service.database import talk_to_db, generate_random_url
from fastapi import APIRouter
from fastapi.responses import RedirectResponse


SHORT_URL_LENGTH = 8

router = APIRouter(prefix="/api", tags=["url_actions"])


@router.post("/shorten_url")
async def shorten_url(record: PostURL):
    if record.custom_url:
        # Custom url provided, proceed with posting to DB
        db_response = talk_to_db("post", record.custom_url, record.original_url)

    else:
        # No custom url provided, need to generate random short url
        while True:
            random_full_url = generate_random_url()
            random_short_url = random_full_url
            # random_short_url = str(random_full_url)[:SHORT_URL_LENGTH]
            db_response = talk_to_db("post", random_short_url, record.original_url)
            if db_response["status_code"] == 200:
                # placeholder if statement
                break

    return db_response["message"]


@router.get("/list_urls")
async def list_urls():
    db_response = talk_to_db("get_all")
    if db_response["status_code"] != 200:
        return db_response["message"]
    else:
        return db_response["payload"]


@router.get("/redirect")
async def redirect(record: GetURL):
    db_response = talk_to_db("get_one", record.short_url)
    if db_response["status_code"] != 200:
        return db_response["message"]
    else:
        url_to_go_to = db_response["payload"]
        return RedirectResponse(url=url_to_go_to, status_code=303)
