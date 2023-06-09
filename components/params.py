from pydantic import BaseModel


class LLMRequest(BaseModel):
    place: str
