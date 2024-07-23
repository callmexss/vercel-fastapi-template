from pydantic import BaseModel


class SimpleQuery(BaseModel):
    content: str
