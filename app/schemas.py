from pydantic import BaseModel
from typing import Optional


class PostRequest(BaseModel):
    post_type: Optional[str] = None
    emotion: Optional[str] = None
    audience: Optional[str] = None
    angle: Optional[str] = None
    word_limit: int = 100


class PostResponse(BaseModel):
    content: str


class FacebookPostRequest(BaseModel):
    content: str


class FacebookPostResponse(BaseModel):
    post_id: str



class GenerateAndPostRequest(BaseModel):
    post_type: Optional[str] = None
    emotion: Optional[str] = None
    audience: Optional[str] = None
    angle: Optional[str] = None
    word_limit: int = 100


class GenerateAndPostResponse(BaseModel):
    content: str
    facebook_post_id: str