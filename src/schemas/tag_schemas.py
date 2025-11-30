from pydantic import BaseModel

class TagBase(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    tag: str | None = None
    timestamp: int | None = None

class TagSchema(TagBase):
    id: int

    model_config = {
        "from_attributes": True
    }