from app.models.pydantic_models import PostURL
from app.service.database import add_custom_url_to_db, add_random_url_to_db, get_all_urls, get_one_url
from fastapi import APIRouter, Path, Body
from typing import Annotated
from fastapi.responses import RedirectResponse


# Temporary return messages
SUCCESS_MESSAGE = "Process successful!"
ERROR_MESSAGE = "Sorry, we could not process your request."

router = APIRouter(prefix="/api", tags=["url_actions"])


@router.post("/shorten_url")
async def shorten_url(record: Annotated[PostURL, Body(title="Pydantic Model for URL")]):
    if record.custom_url:
        # Custom url provided, attempt to add custom url to DB
        response = add_custom_url_to_db(custom_url=record.custom_url, original_url=record.original_url)

    else:
        # No custom url provided, attempt to add randomly generated short url to DB
        response = add_random_url_to_db(original_url=record.original_url)

    if response["status_code"] == 200:
        response["message"] = SUCCESS_MESSAGE
    else:
        response["message"] = ERROR_MESSAGE + f" Error code: {response['status_code']} - {response['payload']}"

    return response


@router.get("/list_urls")
async def list_urls():
    response = get_all_urls()

    if response["status_code"] == 200:
        response["message"] = SUCCESS_MESSAGE
    else:
        response["message"] = ERROR_MESSAGE + f" Error code: {response['status_code']} - {response['payload']}"

    return response


@router.get("/redirect/{short_url}")
async def redirect(short_url: Annotated[str, Path(title="Short URL")] = None):
    if not short_url:
        return {"status_code": 400, "payload": "Bad Input"}

    # Check DB for short_url key
    response = get_one_url(short_url)

    if response["status_code"] == 200:
        response["message"] = SUCCESS_MESSAGE
        url_item = response["payload"]
        if url_item and type(url_item) != str:
            url_to_go_to = url_item.original_url
            return RedirectResponse(url=url_to_go_to, status_code=303)

    else:
        response["message"] = ERROR_MESSAGE + f" Error code: {response['status_code']} - {response['payload']}"

    return response
