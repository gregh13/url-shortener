from pydantic import BaseModel


class PostURL(BaseModel):
    original_url: str
    custom_url: str | None = None


class User(BaseModel):
    email: str
    admin: bool | None = False
    disabled: bool | None = False

