from pydantic import BaseModel


class PostURL(BaseModel):
    original_url: str
    custom_url: str | None = None


class User(BaseModel):
    email: str
    admin: bool | None = False
    disabled: bool | None = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    hashed_password: str
