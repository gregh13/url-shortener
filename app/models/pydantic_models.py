from pydantic import BaseModel


class PostURL(BaseModel):
    original_url: str
    custom_url: str | None = None


# class GetURL(BaseModel):
#     short_url: str
