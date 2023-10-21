from pydantic import ValidationError
from pathlib import Path
from pydantic_settings import BaseSettings,  SettingsConfigDict
from dotenv import load_dotenv
import os


load_dotenv(str(Path(__file__).parent.parent / '.env'), override=False)

stage = os.getenv("CHATBOT_CHATLOG_STAGE", "prod")
print("Build stage: ", stage)

ENV_MAP = {
    "dev": str(Path(__file__).parent.parent /".env.dev"),
    "qa": str(Path(__file__).parent.parent /".env.qa"),
    "prod": str(Path(__file__).parent.parent /".env.prod"),
}

if stage=="dev":
  # Overriding environment variables for dev and qa stages
  load_dotenv(ENV_MAP[stage], override=True)

class APISettings(BaseSettings):
    """
    API settings configuration class.

    This class represents the configuration settings for the API. It inherits from
    `BaseSettings` provided by the `pydantic` library and defines various attributes
    to configure the API behavior.

    Attributes:
        - API_KEY (str): The API key used for authentication. Default is "secret".
        - ALG (str): The algorithm used for token generation or validation. Default is "HS512".
        - model_config (SettingsConfigDict): A configuration dictionary for loading
          environment variables and settings from a .env file. This can be used to
          customize the behavior of the API based on environment-specific settings.

    Example Usage:
        # Creating an instance of APISettings
        api_settings = APISettings()

    Note:
        - This class is designed to be used for configuring an API and customizing its
          behavior based on the provided attributes.
        - The default values of attributes can be overridden by setting environment
          variables or using a .env file.
    """
    API_KEY: str = "secret"
    ALG: str = "HS512"
    model_config = SettingsConfigDict(
        env_file=ENV_MAP[stage],
        env_file_encoding='utf-8', 
        case_sensitive=True,
        extra='ignore'
        )

class ChatDBSettings(BaseSettings):
    """
    Chat database settings configuration class.

    This class represents the configuration settings for a chat database. It inherits from
    `BaseSettings` provided by the `pydantic` library and defines various attributes to
    configure the database connection and specify database-related settings.

    Attributes:
        - MONGO_CHATLOG_USERNAME (str): The username used for MongoDB authentication.
          Default is "nonroot".
        - MONGO_CHATLOG_PASSWORD (str): The password associated with the MongoDB user.
          Default is "secret".
        - MONGO_CHAT_DB_HOST (str): The hostname or IP address of the MongoDB server.
          Default is "172.17.0.1".
        - MONGO_CHAT_DB_PORT (str): The port number on which the MongoDB server is running.
          Default is "27017".
        - MONGO_CHATLOG_DB_NAME (str): The name of the MongoDB database to connect to.
          Default is "chatlog".
        - MONGO_CHATLOG_COLLECTION_MESSAGES (str): The name of the collection in the
          MongoDB database where chat messages are stored.
        - MONGO_CHATLOG_COLLECTION_SESSIONS (str): The name of the collection in the
          MongoDB database where chat sessions are stored.
        - MONGO_CHATLOG_COLLECTION_FEEDBACK (str): The name of the collection in the
          MongoDB database where feedback data is stored.
        - MONGO_CHATLOG_COLLECTION_TICKETS (str): The name of the collection in the
          MongoDB database where support tickets are stored.
        - model_config (SettingsConfigDict): A configuration dictionary for loading
          environment variables and settings from a .env file. This can be used to
          customize the behavior of the database connection based on environment-specific
          settings.

    Example Usage:
        # Creating an instance of ChatDBSettings
        db_settings = ChatDBSettings()

    Note:
        - This class is designed to be used for configuring database-related settings for
          a chat application.
        - The default values of attributes can be overridden by setting environment
          variables or using a .env file to customize the database connection settings.
    """
    # MONGO DB   
    MONGO_CHATLOG_DB_USERNAME: str = "nonroot"
    MONGO_CHATLOG_DB_PASSWORD: str = "secret"
    MONGO_CHATLOG_DB_HOST: str = "172.17.0.1"
    MONGO_CHATLOG_DB_PORT: str = "27017"
    # DB NAME
    MONGO_CHATLOG_DB_NAME: str = "chatlog"
    # MONGO  COLLECTIONS
    MONGO_CHATLOG_COLLECTION_MESSAGES: str = "messages"
    MONGO_CHATLOG_COLLECTION_SESSIONS: str = "sessions"
    MONGO_CHATLOG_COLLECTION_FEEDBACK: str = "feedback"
    MONGO_CHATLOG_COLLECTION_TICKETS: str = "tickets"
    MONGO_CHATLOG_DB_PEM_PATH: str = str(Path(__file__).parent.parent / 'certs/global-bundle.pem')
    # env config
    model_config = SettingsConfigDict(
        env_file=ENV_MAP[stage],
        env_file_encoding='utf-8', 
        case_sensitive=True,
        extra='ignore'
        )
class MetricsDBSettings(BaseSettings):
    """
    Metrics database settings configuration class.

    This class represents the configuration settings for a metrics database. It inherits
    from `BaseSettings` provided by the `pydantic` library and defines various attributes
    to configure the metrics database and specify types of metrics data.

    Attributes:
        - MONGO_MESSAGES_TYPE (str): The type identifier for messages metrics in the
          metrics database.
        - MONGO_SESSIONS_TYPE (str): The type identifier for sessions metrics in the
          metrics database.
        - MONGO_TICKETS_TYPE (str): The type identifier for support tickets metrics in
          the metrics database.
        - MONGO_TICKETSP_TYPE (str): The type identifier for premium support tickets
          metrics in the metrics database.
        - MONGO_AVG_MESSAGES_TYPE (str): The type identifier for average messages metrics
          in the metrics database.
        - MONGO_KEYWORDS_TYPE (str): The type identifier for keywords metrics in the
          metrics database.
        - MONGO_TOPICS_TYPE (str): The type identifier for topics metrics in the metrics
          database.
        - model_config (SettingsConfigDict): A configuration dictionary for loading
          environment variables and settings from a .env file. This can be used to
          customize the behavior of the metrics database based on environment-specific
          settings.

    Example Usage:
        # Creating an instance of MetricsDBSettings
        metrics_settings = MetricsDBSettings()

    Note:
        - This class is designed to be used for configuring settings related to a metrics
          database, including the types of metrics data stored.
        - The default values of attributes can be overridden by setting environment
          variables or using a .env file to customize the metrics database configuration.
    """
    # METRICS TYPE
    MONGO_MESSAGES_TYPE: str="messages"
    MONGO_SESSIONS_TYPE: str="sessions"
    MONGO_TICKETS_TYPE: str="tickets"
    MONGO_TICKETSP_TYPE: str="ticketsp"
    MONGO_AVG_MESSAGES_TYPE: str="avg_messages"
    MONGO_KEYWORDS_TYPE: str="keywords"
    MONGO_TOPICS_TYPE: str="topics"
    model_config = SettingsConfigDict(
        env_file=ENV_MAP[stage],
        env_file_encoding='utf-8', 
        case_sensitive=True,
        extra='ignore'
        )

class Settings(BaseSettings, extra = 'ignore'):
    """
    Application settings configuration class.

    This class represents the configuration settings for an application. It inherits from
    `BaseSettings` provided by the `pydantic` library and defines attributes to configure
    various aspects of the application, including database settings, API settings, metrics
    settings, and a configuration dictionary for loading environment variables from a
    .env file.

    Attributes:
        - db (ChatDBSettings): An instance of `ChatDBSettings` that holds database-related
          configuration settings.
        - api (APISettings): An instance of `APISettings` that holds API-related
          configuration settings.
        - metrics (MetricsDBSettings): An instance of `MetricsDBSettings` that holds
          metrics database-related configuration settings.
        - model_config (SettingsConfigDict): A configuration dictionary for loading
          environment variables and settings from a .env file. This can be used to
          customize various aspects of the application's behavior based on environment-
          specific settings.

    Example Usage:
        # Creating an instance of Settings
        app_settings = Settings()

    Note:
        - This class is designed to be used for configuring various aspects of an
          application, including its database, API, and metrics settings.
        - It provides a structured way to access and manage application configuration.
        - The default values of attributes can be overridden by setting environment
          variables or using a .env file to customize the application's behavior.
    """
    db: ChatDBSettings = ChatDBSettings()
    api: APISettings = APISettings()
    metrics: MetricsDBSettings = MetricsDBSettings()
    model_config = SettingsConfigDict(
        env_file=ENV_MAP[stage],
        env_file_encoding='utf-8', 
        case_sensitive=True,
        extra='ignore'
        )

try:
    # Creating an instance of Settings to be imported by other modules
    settings = Settings()
except ValidationError as e:
    # Print validation error if there is an issue with the settings
    print(e)