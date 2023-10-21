from core.models.base_model import BaseDTO, generate_id, generate_date_str
from pydantic import  Field
from typing import Optional, List


class Elements(BaseDTO):
    type: Optional[str] = None
    label: Optional[str] = None
    value: Optional[str] = None
    background_color: Optional[str] = Field(default="#FFFFFF", alias="backgroundColor")
    text_color: Optional[str] = Field(default="#000000", alias="textColor")

class ChatMessage(BaseDTO):
    timestamp: Optional[str] = Field(default_factory=generate_date_str)
    message_id: Optional[str] = Field(default_factory=generate_id, alias="messageID")
    session_id: Optional[str] = Field(default=None, alias="sessionID")
    text: Optional[str] = None
    elements: Optional[List[Elements]] = None
    user: Optional[str] = None
    feedback: Optional[bool] = False


class ApplicationData(BaseDTO):
    email: Optional[str] = Field(default=None, alias="sub")
    role: Optional[str] = Field(default=None, alias="auth")
    name: Optional[str] = Field(default=None, alias="fn")
    last_name: Optional[str] = Field(default=None, alias="ln")
    