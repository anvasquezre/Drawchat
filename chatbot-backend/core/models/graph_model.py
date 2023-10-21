from .base_model import BaseDTO
from typing import Dict, List
from pydantic import Field, AliasChoices

class ConnectionOutput(BaseDTO):
    node: str = None
    output: str = None
    
class ConnectionInput(BaseDTO):
    node: str = None
    input: str = None

class Output(BaseDTO):
    connections: List[ConnectionOutput] = []

class Input(BaseDTO):
    connections: List[ConnectionInput] = []

class NodeData(BaseDTO):
    id: int
    name: str
    data: Dict
    class_: str = Field(alias=AliasChoices("class"),serialization_alias="class")
    html: str
    typenode: bool
    inputs: Dict[str, Input]
    outputs: Dict[str, Output]
    pos_x: float
    pos_y: float

class Flow(BaseDTO):
    data: Dict[str, NodeData]

class Root(BaseDTO):
    drawflow: Dict[str,Flow]