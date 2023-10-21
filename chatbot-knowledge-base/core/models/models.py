
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import uuid
from core.settings import settings


def generate_id():
    """
    Generate a unique identifier (UUID).

    This function generates a universally unique identifier (UUID) and returns it as a
    string. UUIDs are unique across space and time, making them suitable for various
    purposes, including as unique identifiers for database records, objects, or entities.

    Returns:
        str: A string representation of the generated UUID.

    Example Usage:
        unique_id = generate_id()

    Note:
        - UUIDs generated by this function are typically 36 characters long and have a
          format like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
        - The probability of generating the same UUID twice is extremely low, making
          UUIDs suitable for unique identification purposes.
    """
    return str(uuid.uuid4())



class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra='ignore',
        complete=False,
        populate_by_name = True
    )
    
        
    
class UpdateQuery(BaseDTO):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
class UpdateResponse(UpdateQuery):
    num_docs: int = None

class DocumentDTO(BaseDTO):
    page_content: str = None
    metadata: Dict[str, Any] = None
    score: float = None
    
class DocumentListDTO(BaseDTO):
    documents: List[DocumentDTO] = None
    num_docs: int = None

class ModelKwargs(BaseDTO):
    temperature: float = Field(default=settings.openai_kwargs.temperature)
    max_tokens: int = Field(default=settings.openai_kwargs.max_tokens)

class DocumentQuery(BaseDTO):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model: str = Field(default=settings.openai.MODEL)
    llm_model_kwargs: ModelKwargs = ModelKwargs()
    question: str = None
    generate: bool = True
    num_results: int = 5
    score_threshold: float = 0.3
    

    
    
class DocumentQueyResponse(DocumentQuery):
    answer: str | None = None
    documents: List[DocumentDTO] = None
    
class GenerateQuery(BaseDTO):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model: str = Field(default=settings.openai.MODEL)
    llm_model_kwargs: ModelKwargs = ModelKwargs()
    system_prompt: str = Field(default="You are a useful assistant")
    human_prompt: str
    
class GenerateResponse(GenerateQuery):
    answer: str | None = None