from pydantic import BaseModel, ConfigDict
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    title: str
    published: bool = True
    rating: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
