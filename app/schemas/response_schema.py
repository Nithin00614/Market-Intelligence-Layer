from pydantic import BaseModel

class MarketResponse(BaseModel):

    company: str
    final_report: str