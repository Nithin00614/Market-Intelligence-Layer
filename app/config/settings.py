import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    FINANCIAL_API_KEY = os.getenv("FINANCIAL_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME")

settings = Settings()