from pydantic import ValidationError
from pathlib import Path
from pydantic_settings import BaseSettings,  SettingsConfigDict
from dotenv import load_dotenv
from typing import List
import os


load_dotenv(str(Path(__file__).parent.parent / '.env'), override=False)

stage = os.getenv("CHATBOT_KNOWLEDGEBASE_STAGE", "prod")
print("Build stage: ", stage)

ENV_MAP = {
    "dev": str(Path(__file__).parent.parent /".env.dev"),
    "qa": str(Path(__file__).parent.parent /".env.qa"),
    "prod": str(Path(__file__).parent.parent /".env.prod"),
}

if stage=="dev":
  # Overriding environment variables for dev and qa stages
  load_dotenv(ENV_MAP[stage], override=True)
  
class CoreSettings(BaseSettings):
  model_config = SettingsConfigDict(
        env_file=ENV_MAP[stage],
        env_file_encoding='utf-8', 
        case_sensitive=True,
        extra='ignore'
        )
  
class APISettings(CoreSettings):

    API_KEY: str = "secret"
    ALG: str = "HS512"


class QdrantSettings(CoreSettings):
  """

  Args:
      BaseSettings (_type_): _description_
  """
  QDRANT_HOST: str = "localhost"
  QDRANT_PORT: str = "6333"
  QDRANT_GRPC_PORT: str = "6334"
  QDRANT_USE_HTTPS: bool = False
  COLLECTIONS : list = ["index"]
  model_config = SettingsConfigDict(
        env_file=ENV_MAP[stage],
        env_file_encoding='utf-8', 
        case_sensitive=True,
        extra='ignore'
        )

class OpenAISettings(CoreSettings):
  OPENAI_API_KEY: str = "secret"
  MODEL: str = "gpt-3.5-turbo"
  
class OpenAIKwargsSettings(CoreSettings):
    """
    Settings for OpenAI summarization model keyword arguments.

    Attributes:
        temperature (float): The temperature parameter for the model.
        max_tokens (int): The maximum number of tokens for model output.
    """
    temperature: float = 0.5
    max_tokens: int = 2000

class Settings(CoreSettings, extra = 'ignore'):

    api: APISettings = APISettings()
    qdrant : QdrantSettings = QdrantSettings()
    openai: OpenAISettings = OpenAISettings()
    openai_kwargs: OpenAIKwargsSettings = OpenAIKwargsSettings()


try:
    # Creating an instance of Settings to be imported by other modules
    settings = Settings()
    if stage=="dev":
      print("Settings: ", settings.model_dump())
    
except ValidationError as e:
    # Print validation error if there is an issue with the settings
    print(e)