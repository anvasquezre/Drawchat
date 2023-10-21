
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import uuid
from core.settings import settings
from core.models.base_model import generate_date_str




class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra='ignore',
        complete=False,
        populate_by_name = True
    )
    
        
    
class UpdateQuery(BaseDTO):
    timestamp: str = Field(default_factory=generate_date_str)
    
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
    timestamp: str = Field(default_factory=generate_date_str)
    model: str = Field(default=settings.openai.MODEL)
    llm_model_kwargs: ModelKwargs = ModelKwargs()
    question: str = None
    generate: bool = True
    num_results: int = 5
    

    
    
class DocumentQueyResponse(DocumentQuery):
    answer: str | None = None
    documents: List[DocumentDTO] = None
    
class GenerateQuery(BaseDTO):
    timestamp: str = Field(default_factory=generate_date_str)
    model: str = Field(default=settings.openai.MODEL)
    llm_model_kwargs: ModelKwargs = ModelKwargs()
    system_prompt: str = Field(default="You are a useful assistant")
    human_prompt: str
    
class GenerateResponse(GenerateQuery):
    answer: str | None = None