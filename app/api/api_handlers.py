from app.models.pydantic_models import PostURL
from app.service.database import add_custom_url_to_db, add_random_url_to_db, get_all_urls, get_one_url
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

# Temporary return messages
SUCCESS_MESSAGE = "Process successful!"
ERROR_MESSAGE = "Sorry, we could not process your request"

router = APIRouter(prefix="/api", tags=["url_actions"])


@router.post("/shorten_url")
async def shorten_url(record: PostURL):
    if record.custom_url:
        # Custom url provided, attempt to add custom url to DB
        db_response = add_custom_url_to_db(custom_url=record.custom_url, original_url=record.original_url)

    else:
        # No custom url provided, attempt to add randomly generated short url to DB
        db_response = add_random_url_to_db(original_url=record.original_url)

    if db_response == 201:
        return SUCCESS_MESSAGE

    else:
        return f"{ERROR_MESSAGE} --> status code: {db_response}"


@router.get("/list_urls")
async def list_urls():
    db_response = get_all_urls()
    if db_response["status_code"] == 200:
        # Request to DB was successful, return
        return db_response["payload"]

    else:
        # Bad response, DB not reachable
        return f"{ERROR_MESSAGE} --> status code: {db_response}"


@router.get("/redirect/{short_url}")
async def redirect(short_url: str):
    if not short_url:
        return f"{ERROR_MESSAGE} --> status code: 400"

    # Check DB for short_url key
    db_response = get_one_url(short_url)

    if db_response["status_code"] == 200:
        url_to_go_to = db_response["payload"]
        return RedirectResponse(url=url_to_go_to, status_code=303)

    else:
        return f"{ERROR_MESSAGE} --> status code: {db_response}"
