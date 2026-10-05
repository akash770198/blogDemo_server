from pydantic import BaseModel, ConfigDict


class BlogCreate(BaseModel):
    title: str
    content: str


class BlogResponse(BlogCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
