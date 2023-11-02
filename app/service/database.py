from app.models.pynamo_models import Thread
from pynamodb.exceptions import PutError
from uuid import uuid4

SHORT_URL_LENGTH = 8
MAX_RANDOM_URL_ATTEMPTS = 50


def add_item_to_db(short_url, original_url):
    # Create key:value pair to add to DB
    new_item = Thread(short_url=short_url, original_url=original_url)

    try:
        # Create condition to make sure Short Url isn't already in DB
        condition = Thread.short_url.does_not_exist()

        # Attempt to add item to DB
        new_item.save(condition=condition)

    except PutError:
        # Condition failed, Short Url already exists in DB
        return 409

    else:
        # Short Url was successfully added to DB
        return 201


def talk_to_db(type: str, foo = None, bar = None):
    # placeholder function
    return {
        "status_code": 200,
        "message": "Some message",
        "payload": "https://www.google.com"
            }


def generate_valid_random_url(original_url):
    # Initialize attempts to create and add random url to DB
    attempts = 1

    while attempts < MAX_RANDOM_URL_ATTEMPTS:
        # Generate secure random uuid
        random_full_url = uuid4()

        # Truncate long uuid to shorter random string
        random_short_url = str(random_full_url)[:SHORT_URL_LENGTH]

        # Try to add url to DB
        response = add_item_to_db(short_url=random_short_url, original_url=original_url)

        # Break while loop once url has been successfully added to DB
        if response == 201:
            break

        # Increment attempts and try again with a new random url
        attempts += 1

    else:
        # Block only triggers after too many failed attempts
        return

    # This is only reachable when random url is successfully added to DB
    return
