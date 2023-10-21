from pydantic import ValidationError
from pathlib import Path
from pydantic_settings import BaseSettings,  SettingsConfigDict
from dotenv import load_dotenv
import os


load_dotenv(str(Path(__file__).parent.parent / '.env'), override=False)

stage = os.getenv("CHATBOT_BACKEND_STAGE", "prod")
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
  
class OpenAISettings(CoreSettings):
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
  
class APISettings(CoreSettings):
    # TODO  protect endpoints with JWT
    ALG: str = "HS512"
    SECRET : str = "secret"
    ORIGINS : list = ["*"]

class KnowledgeBaseSettings(CoreSettings):
  
  CHATBOT_KB_URL: str = "http://localhost:8000/api/v1"
  CHATBOT_KB_TOKEN: str = "token"

class FreshDeskSettings(CoreSettings):
  FRESHDESK_API_KEY: str = "key"
  FRESHDESK_API_DOMAIN: str = "domain"
  FRESHDESK_API_PASSWORD : str = "password"

class ChatbotChatlogSettings(CoreSettings):
  CHATBOT_CHATLOG_URL: str = "http://localhost:8000/api/v1"
  CHATBOT_CHATLOG_TOKEN: str = "token"

class Settings(CoreSettings):

    api: APISettings = APISettings()
    openai: OpenAISettings = OpenAISettings()
    openai_kwargs: OpenAIKwargsSettings = OpenAIKwargsSettings()
    kb: KnowledgeBaseSettings = KnowledgeBaseSettings()
    freshdesk: FreshDeskSettings = FreshDeskSettings()
    chatlog: ChatbotChatlogSettings = ChatbotChatlogSettings()
try:
    # Creating an instance of Settings to be imported by other modules
    settings = Settings()
except ValidationError as e:
    # Print validation error if there is an issue with the settings
    print(e)