from pydantic import BaseModel


class PostURL(BaseModel):
    original_url: str
    custom_url: str | None = None


class User(BaseModel):
    username: str
    hashed_password: str
    url_limit: int | None = 20
    user_urls: list[dict] | None = []
    admin: bool | None = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
