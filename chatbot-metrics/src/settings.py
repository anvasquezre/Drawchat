import os
from pathlib import Path
from typing import Optional
from pydantic import ValidationError

from pydantic_settings import BaseSettings,  SettingsConfigDict
from dotenv import load_dotenv
import os
# For local development, load environment variables from a .env file
# For production, environment variables should be set directly in the environment, override=False
load_dotenv(str(Path(__file__).parent.parent / '.env'), override=False)

stage = os.getenv("CHATBOT_METRICS_STAGE", "prod")
print("Running in stage: ", stage)

ENV_MAP = {
    "dev": str(Path(__file__).parent.parent /".env.dev"),
    "qa": str(Path(__file__).parent.parent /".env.qa"),
    "prod": str(Path(__file__).parent.parent /".env.prod"),
}

if stage=="dev":
  # Overriding environment variables for dev and qa stages
  load_dotenv(ENV_MAP[stage], override=True)

class DefaultMetrics(BaseSettings):
    """
    Default Metrics Configuration.

    This class defines the default metrics configuration, including a list of metric types
    that can be used in the application.

    Attributes:
        - metric_list (list[str]): A list of metric types including "messages," "sessions," "tickets,"
          "ticketsp," "avg_messages," "keywords," and "topics."

    Example Usage:
        metrics = DefaultMetrics()
        print(metrics.metric_list)
    """
    metric_list: list[str] = ["messages","sessions","tickets","ticketsp","avg_messages","keywords","topics"]


class APISettings(BaseSettings):
    """
    API Settings Configuration.

    This class defines the API settings configuration, including API URI, API token, resources path,
    and model configuration.

    Attributes:
        - API_URI (str): The base URI for the API endpoint.
        - API_TOKEN (str): The API authentication token.
        - RESOURCES_PATH (str): The path to the resources directory.
        - model_config (SettingsConfigDict): Configuration for loading environment variables
          from a .env file.

    Example Usage:
        api_settings = APISettings()
        print(api_settings.API_URI)
    """
    # METRICS TYPE
    API_URI: str = "http://172.17.0.1:3000/api/v1"
    API_TOKEN : str = "secret"
    RESOURCES_PATH: str = str(Path(os.path.join(os.path.dirname(__file__), 'resources')))
    model_config = SettingsConfigDict(
        env_file=ENV_MAP[stage],
        env_file_encoding='utf-8', 
        case_sensitive=True,
        extra='ignore'
        )

class LoggingSettings(BaseSettings):
    SECRET: str = "secret"
    LOGIN_URL: str = "http://localhost:9000"
    model_config = SettingsConfigDict(
        env_file=ENV_MAP[stage],
        env_file_encoding='utf-8', 
        case_sensitive=True,
        extra='ignore'
        )
class Settings(BaseSettings, extra = 'ignore'):
    """
    Application Settings Configuration.

    This class defines the application settings configuration, including API settings and default metrics.

    Attributes:
        - api (APISettings): An instance of APISettings containing API-related configuration.
        - metrics (DefaultMetrics): An instance of DefaultMetrics containing default metrics configuration.

    Example Usage:
        settings = Settings()
        print(settings.api.API_URI)
    """
    api: APISettings = APISettings()
    metrics: DefaultMetrics = DefaultMetrics()
    login: LoggingSettings = LoggingSettings()
    model_config = SettingsConfigDict(
        env_file=ENV_MAP[stage],
        env_file_encoding='utf-8', 
        case_sensitive=True,
        extra='ignore'
        )
# Load the settings from the .env file
try:
    # Load the settings from the .env file
    settings = Settings()
# If there is an error, print it
except ValidationError as e:
    print(e)


# Define the mapping between metric types and metric names
METRICS_MAPPING = {
    "Messages": "messages",
    "Sessions": "sessions",
    "Tickets": "tickets",
    # "Tickets per session": "ticketsp",
    # "Average messages per session": "avg_messages",
    "Keywords": "keywords",
    "AI Topics": "topics"
}
# Define the mapping between intervals types and sampling periods
SAMPLING_MAPPING = {
    "Hourly": "1h",
    "Daily": "1d",
    "Weekly": "1w",
    "Monthly": "1m",
    "Yearly": "1y"
}