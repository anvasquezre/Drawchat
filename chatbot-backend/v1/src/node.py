from typing import List, Optional, Callable
from pydantic import BaseModel, ConfigDict, Field

from ..utils.utils import generate_uuid


class Node(BaseModel):
    name: str = Field(alias="name")
    id: Optional[str] = Field(default_factory=generate_uuid)
    type: Optional[str | None] = None
    handler: Optional[Callable] = None
    data: Optional[dict] = {}
    children: Optional[List[str]] = []
    parents: Optional[List[str]] = []
    pos_x: Optional[float] = None
    pos_y: Optional[float] = None
    
    model_config = ConfigDict(
        extra="ignore",
    )

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parents.append(parent)
        
    def execute(self, value):
        if self.handler is not None:
            text = self.handler(value)
            return text
        
    def to_dict(self):
        return self.model_dump()