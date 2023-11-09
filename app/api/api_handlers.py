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
        response = add_custom_url_to_db(custom_url=record.custom_url, original_url=record.original_url)

    else:
        # No custom url provided, attempt to add randomly generated short url to DB
        response = add_random_url_to_db(original_url=record.original_url)

    return f"{response["status_code"]}: {response["payload"]}"


@router.get("/list_urls")
async def list_urls():
    response = get_all_urls()
    if response["status_code"] == 200:
        # Request to DB was successful, return
        return response["payload"]

    else:
        # Bad response, DB not reachable
        return f"{ERROR_MESSAGE} --> status code: {response["status_code"]}"


@router.get("/redirect/{short_url}")
async def redirect(short_url: str):
    if not short_url:
        return f"{ERROR_MESSAGE} --> status code: 400"

    # Check DB for short_url key
    response = get_one_url(short_url)

    if response["status_code"] == 200:
        url_item = response["payload"]
        if url_item and type(url_item) != str:
            url_to_go_to = url_item.original_url
            return RedirectResponse(url=url_to_go_to, status_code=303)

    return f"{ERROR_MESSAGE} --> status code: {response}"
