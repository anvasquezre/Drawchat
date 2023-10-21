
from pydantic import Field
from typing import Dict, Optional
import uuid
from .base_model import BaseDTO
from .graph_model import Root
from core.models.base_model import generate_id


class Workflow(BaseDTO):
    id: str = Field(default_factory=generate_id)
    graph: Root = None
    
    