from app.models.pynamo_models import Thread
from pynamodb.exceptions import AttributeNullError, DeleteError, DoesNotExist, PutError, PynamoDBConnectionError
from uuid import uuid4

SHORT_URL_LENGTH = 8
MAX_RANDOM_URL_ATTEMPTS = 50


def add_url_to_db(short_url, original_url):
    # Initialize response
    response = {
        "status_code": None,
        "payload": ''
    }

    # Create key:value pair to add to DB
    new_item = Thread(short_url=short_url, original_url=original_url)

    try:
        # Create condition to make sure Short Url isn't already in DB
        condition = Thread.short_url.does_not_exist()

        # Attempt to add item to DB
        new_item.save(condition=condition)

    except AttributeNullError:
        # Bad request, short_url is Null
        response["payload"] = "AttributeNullError"
        response["status_code"] = 400

    except TypeError:
        # Bad request, short_url is invalid
        response["payload"] = "TypeError"
        response["status_code"] = 400

    except PutError:
        # Condition failed, Short Url already exists in DB
        response["payload"] = "PutError"
        response["status_code"] = 409

    except PynamoDBConnectionError:
        # Internal Server Error, unreachable server
        response["payload"] = "DBConnectionError"
        response["status_code"] = 500

    else:
        # Success, short Url was successfully added to DB
        response["payload"] = "Success"
        response["status_code"] = 200

    return response


def add_custom_url_to_db(custom_url, original_url):
    return add_url_to_db(short_url=custom_url, original_url=original_url)


def add_random_url_to_db(original_url):
    # Initialize response
    response = {
        "status_code": None,
        "payload": ''
    }

    # Initialize attempts to create and add random url to DB
    attempts = 1

    while attempts < MAX_RANDOM_URL_ATTEMPTS:
        # Generate secure random uuid
        random_full_url = uuid4()

        # Truncate long uuid to shorter random string
        random_short_url = str(random_full_url)[:SHORT_URL_LENGTH]

        # Try to add url to DB
        response = add_url_to_db(short_url=random_short_url, original_url=original_url)

        # Check if url was successfully added to DB
        if response["status_code"] == 200:
            return response

        # Increment attempts and try again with a new random url
        attempts += 1

    # Max attempts reached, failed to add url to DB
    return response


def delete_item(short_url):
    # Initialize response
    response = {
        "status_code": None,
        "payload": []
    }

    # Need to get actual item in order to delete item
    response = get_one_url(short_url=short_url)

    if response["status_code"] == 200:
        # item retrieved, can now try to delete
        try:
            item_to_delete = response["payload"]
            item_to_delete.delete()

        except DeleteError:
            # Failed to delete
            response["payload"] = "DeleteError"
            response["status_code"] = 501

        else:
            # Success, url deleted
            response["payload"] = "Successfully Deleted Item"
            response["status_code"] = 200

    return response


def get_all_urls():
    # Initialize response
    response = {
        "status_code": None,
        "payload": []
    }

    try:
        # Get all urls in DB
        all_url_items = Thread.scan()

    except PynamoDBConnectionError:
        # Internal Server Error, unreachable server
        response["payload"] = "DBConnectionError"
        response["status_code"] = 500

    else:
        # Success, all urls retrieved
        response["status_code"] = 200

        # Add urls to payload
        for url_item in all_url_items:
            url = {
                "short_url": url_item.short_url,
                "original_url": url_item.original_url
            }

            response["payload"].append(url)

    return response


def get_one_url(short_url):
    # Initialize response
    response = {
        "status_code": None,
        "payload": ''
    }

    try:
        # Get url key pair in DB
        url_item = Thread.get(short_url)

    except TypeError:
        # Bad request, issue with getting item from DB
        response["payload"] = "TypeError"
        response["status_code"] = 400

    except PynamoDBConnectionError:
        # Internal Server Error, unreachable server
        response["payload"] = "DBConnectionError"
        response["status_code"] = 500

    except DoesNotExist:
        # Not Found, Url not in DB
        response["payload"] = "DoesNotExist"
        response["status_code"] = 404

    else:
        # Success, url retrieved
        response["payload"] = url_item
        response["status_code"] = 200

    return response


def reset_db():
    response = get_all_urls()

    if response["status_code"] == 200:
        # Remove all entries from DB
        for url in response["payload"]:
            short_url = url["short_url"]
            delete_item(short_url)

        # Repopulate with exisiting url
        add_custom_url_to_db(custom_url="existing_url", original_url="https://www.google.com")

    return response
