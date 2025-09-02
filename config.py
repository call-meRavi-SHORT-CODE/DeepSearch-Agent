from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config(BaseSettings):
    SAMBANOVA_API_KEY: str
    SAMBANOVA_BASE_URL: str
    LLM_REASONING: str
    LLM_REGULAR: str
    TAVILY_API_KEY: str



config = Config(SAMBANOVA_API_KEY=os.environ["SAMBANOVA_API_KEY"],
                SAMBANOVA_BASE_URL="https://api.sambanova.ai/v1",
                LLM_REASONING="DeepSeek-R1-Distill-Llama-70B",
                LLM_REGULAR="Meta-Llama-3.3-70B-Instruct",
                TAVILY_API_KEY=os.environ["TAVILY_API_KEY"])