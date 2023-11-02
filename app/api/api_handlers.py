from app.models.pydantic_models import PostURL, GetURL
from app.service.database import add_url_to_db, add_custom_url_to_db, add_random_url_to_db
from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(prefix="/api", tags=["url_actions"])


@router.post("/shorten_url")
async def shorten_url(record: PostURL):
    if record.custom_url:
        # Custom url provided, attempt to add custom url to DB
        db_response = add_custom_url_to_db(custom_url=record.custom_url, original_url=record.original_url)

    else:
        # No custom url provided, attempt to add randomly generated short url to DB
        db_response = add_random_url_to_db(original_url=record.original_url)

    return db_response


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
