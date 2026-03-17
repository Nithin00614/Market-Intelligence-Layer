
from pydantic import BaseModel

class MarketRequest(BaseModel):

    company: str
    question: str