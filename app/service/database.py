from uuid import uuid4


def talk_to_db(type: str, foo = None, bar = None):
    # placeholder function
    return {
        "status_code": 200,
        "message": "Some message",
        "payload": "https://www.google.com"
            }


def generate_random_url():
    return uuid4()