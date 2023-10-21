
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from typing import Dict, Optional
import uuid


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


class SessionBase(BaseModel):
    """
    Base model for session data.

    This class defines a base data model for capturing session-related information.
    It includes attributes such as session creation and end times, user email, user name,
    user role, user consent, and metadata about the session.

    Attributes:
        - created_at (Optional[datetime]): The timestamp when the session was created.
          Default is the current UTC time.
        - ended_at (Optional[datetime]): The timestamp when the session ended. Default is
          None.
        - user_email (Optional[EmailStr]): The email address of the user associated with
          the session. Default is None.
        - user_name (Optional[str]): The name of the user associated with the session.
          Default is None.
        - user_role (Optional[str]): The role of the user associated with the session.
          Default is None.
        - data_user_consent (Optional[bool]): A flag indicating whether the user has given
          consent for data collection. Default is False.
        - metadata (Optional[SessionMetadata]): Additional metadata about the session,
          such as IP address, device, browser, and OS. Default is None.

    Example Usage:
        # Creating an instance of SessionBase with sample data
        session_data = SessionBase(
            user_email="user@example.com",
            user_name="John Doe",
            user_role="Admin",
            data_user_consent=True,
            metadata=SessionMetadata(
                ip="111.111.11.111",
                device="Mobile/Desktop",
                browser="Chrome",
                os="Windows/Linux/MacOS"
            )
        )

    Note:
        - This class serves as a base model for capturing session data, and its attributes
          can be optional to accommodate various use cases.
        - Example data is provided in the model_config for reference, demonstrating the
          expected structure of session data.
    """
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    user_email: Optional[EmailStr] = None
    user_name: Optional[str] = None
    user_role: Optional[str] = None
    data_user_consent: Optional[bool] = False
    origin: Optional[str] = None
    application_data: Optional[Dict] = None
    metadata: Optional[str] = None
    

    
class SessionCreate(SessionBase):
    """
    Model for creating a session.

    This class extends the base `SessionBase` model and adds an attribute for the
    `session_id`, which represents a unique identifier for the session being created.

    Attributes:
        - session_id (str): A unique identifier for the session. It is generated using
          the `generate_id` function by default.
        
    Example Usage:
        # Creating an instance of SessionCreate with sample data
        session_data = SessionCreate(
            session_id=str(uuid.uuid4()),
            created_at=str(datetime.utcnow()),
            ended_at=datetime.utcnow() + timedelta(minutes=30),
            user_email="user@example.com",
            user_name="John Doe",
            user_role="Owner/Applicant/Realtor",
            data_user_consent=True,
            metadata=SessionMetadata(
                ip="111.111.11.111",
                device="Mobile/Desktop",
                browser="Chrome",
                os="Windows/Linux/MacOS"
            )
        )

    Note:
        - This class is used to represent session data when creating a new session, and
          it includes additional attributes beyond the base `SessionBase`.
        - Example data is provided in the `json_schema_extra` for reference, demonstrating
          the expected structure of session data when creating a session.
    """
    session_id: str = Field(default_factory=generate_id)
    
    class Config:
        json_schema_extra = {
                "examples": [
                    {
                        "session_id": uuid.uuid4(),
                        "created_at": str(datetime.utcnow()),
                        "ended_at": datetime.utcnow()+timedelta(minutes=30),
                        "user_email": "user@email.com",
                        "user_name": "John Doe",
                        "user_role": "Owner/Applicant/Realtor",
                        "data_user_consent": True,
                        "metadata": {
                        "ip": "111.111.11.111",
                        "device": "Mobile/Desktop",
                        "browser": "Chrome",
                        "os": "Windows/Linux/MacOS"
                    }
                        
                    }
                ]
            }


class Session(SessionBase):
    """
    Model representing a session.

    This class extends the base `SessionBase` model and includes an attribute for the
    `session_id`, which represents a unique identifier for the session.

    Attributes:
        - session_id (str): A unique identifier for the session.
        
    Example Usage:
        # Creating an instance of Session with sample data
        session_data = Session(
            session_id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            ended_at=datetime.utcnow() + timedelta(minutes=30),
            user_email="user@example.com",
            user_name="John Doe",
            user_role="Owner/Applicant/Realtor",
            data_user_consent=True,
            metadata=SessionMetadata(
                ip="111.111.11.111",
                device="Mobile/Desktop",
                browser="Chrome",
                os="Windows/Linux/MacOS"
            )
        )

    Note:
        - This class is used to represent a session, including its attributes and
        associated data.
        - Example data is provided in the `json_schema_extra` for reference, demonstrating
        the expected structure of session data.
    """
    session_id: str 
    class Config:
        from_attibutes = True
        json_schema_extra = {
            "examples": [
                {
                    "session_id": uuid.uuid4(),
                    "created_at": datetime.utcnow(),
                    "ended_at": datetime.utcnow()+timedelta(minutes=30),
                    "user_email": "user@email.com",
                    "user_name": "John Doe",
                    "user_role": "Owner/Applicant/Realtor",
                    "data_user_consent": True,
                    "metadata": {
                    "ip": "111.111.11.111",
                    "device": "Mobile/Desktop",
                    "browser": "Chrome",
                    "os": "Windows/Linux/MacOS"
                }
                    
                }
            ]
        }
        
    

class MessageBase(BaseModel):
    """
    Base model for chat messages.

    This class defines a base data model for chat messages. It includes attributes
    such as the message creation timestamp, exchange source, message type, and session ID.

    Attributes:
        - created_at (Optional[datetime]): The timestamp when the message was created.
          Default is the current UTC time.
        - exchange (Optional[str]): The source of the message (e.g., "chat from the user
          or bot"). Default is None.
        - message_type (Optional[str]): The type of message (e.g., "AI/USER"). Default is
          None.
        - session_id (Optional[str]): The session ID associated with the message. Default
          is None.

    Example Usage:
        # Creating an instance of MessageBase with sample data
        message_data = MessageBase(
            created_at=datetime.utcnow(),
            exchange="chat from the user or bot",
            message_type="AI/USER",
            session_id="98766545431"
        )

    Note:
        - This class serves as a base model for chat messages, and its attributes can be
          optional to accommodate various use cases.
    """
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    exchange: Optional[str] = None
    message_type: Optional[str] = None
    session_id: Optional[str] = None

class MessageCreate(MessageBase):
    """
    Model for creating a chat message.

    This class extends the base `MessageBase` model and adds an attribute for the
    `message_id`, which represents a unique identifier for the message being created.

    Attributes:
        - message_id (Optional[str]): A unique identifier for the message. It is generated
          using the `generate_id` function by default.

    Example Usage:
        # Creating an instance of MessageCreate with sample data
        message_data = MessageCreate(
            message_id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            exchange="chat from the user or bot",
            message_type="AI/USER",
            session_id="98766545431"
        )

    Note:
        - This class is used to represent a chat message when creating a new message, and
          it includes additional attributes beyond the base `MessageBase`.
    """
    message_id: Optional[str] = Field(default_factory=generate_id)
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "message_id": uuid.uuid4(),
                    "created_at": datetime.utcnow(),
                    "exchange": "chat from the user or bot",
                    "message_type": "AI/USER",
                    "session_id": "98766545431"
                }
            ]
        }

class Message(MessageBase):
    """
    Model representing a chat message.

    This class extends the base `MessageBase` model and includes an attribute for the
    `message_id`, which represents a unique identifier for the message.

    Attributes:
        - message_id (str): A unique identifier for the message.

    Example Usage:
        # Creating an instance of Message with sample data
        message_data = Message(
            message_id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            exchange="chat from the user or bot",
            message_type="AI/USER",
            session_id="98766545431"
        )

    Note:
        - This class is used to represent a chat message with a specified `message_id`.
        - It is typically used when retrieving or working with existing chat messages.
    """
    
    message_id: str 
    
    class Config:
        from_attibutes = True
        json_schema_extra = {
            "examples": [
                {
                    "message_id": uuid.uuid4(),
                    "created_at": datetime.utcnow(),
                    "exchange": "chat from the user or bot",
                    "message_type": "AI/USER",
                    "session_id": "98766545431"
                }
            ]
        }

class FeedbackBase(BaseModel):
    """
    Base model for feedback data.

    This class defines a base data model for feedback, including attributes such as the
    feedback creation timestamp, session ID, feedback content, feedback stage, and
    additional data.

    Attributes:
        - created_at (Optional[datetime]): The timestamp when the feedback was created.
          Default is None.
        - session_id (Optional[str]): The session ID associated with the feedback. Default
          is None.
        - feedback (Optional[str]): The feedback content (e.g., positive/negative/neutral).
          Default is None.
        - feedback_stage (Optional[str]): The stage at which the feedback was given (e.g.,
          "chat"). Default is None.
        - data (Optional[str]): Additional data related to the feedback. Default is None.

    Example Usage:
        # Creating an instance of FeedbackBase with sample data
        feedback_data = FeedbackBase(
            created_at=datetime.utcnow(),
            session_id="98766545431",
            feedback="positive/negative/neutral",
            feedback_stage="chat",
            data="Optional"
        )

    Note:
        - This class serves as a base model for feedback data, and its attributes can be
          optional to accommodate various use cases.
    """
    
    
    created_at: Optional[datetime] = None
    session_id: Optional[str] = None
    feedback: Optional[str] = None
    feedback_stage: Optional[str] = None
    data: Optional[str] = None
    
class FeedbackCreate(FeedbackBase):
    """
    Model for creating feedback.

    This class extends the base `FeedbackBase` model and adds an attribute for the
    `feedback_id`, which represents a unique identifier for the feedback being created.

    Attributes:
        - feedback_id (Optional[str]): A unique identifier for the feedback. It is
          generated using the `generate_id` function by default.

    Example Usage:
        # Creating an instance of FeedbackCreate with sample data
        feedback_data = FeedbackCreate(
            feedback_id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            session_id="98766545431",
            feedback="positive/negative/neutral",
            feedback_stage="chat",
            data="Optional"
        )

    Note:
        - This class is used to represent feedback data when creating new feedback, and
          it includes additional attributes beyond the base `FeedbackBase`.
    """


    feedback_id: Optional[str] = Field(default_factory=generate_id)
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "feedback_id": uuid.uuid4(),
                    "created_at": datetime.utcnow(),
                    "session_id": "98766545431",
                    "feedback": "positive/negative/neutral",
                    "feedback_stage": "chat",
                    "data": "Optional"
                }
            ]
        }

class Feedback(FeedbackBase):
    """
    Model representing feedback.

    This class extends the base `FeedbackBase` model and includes an attribute for the
    `feedback_id`, which represents a unique identifier for the feedback.

    Attributes:
        - feedback_id (str): A unique identifier for the feedback.

    Example Usage:
        # Creating an instance of Feedback with sample data
        feedback_data = Feedback(
            feedback_id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            session_id="98766545431",
            feedback="positive/negative/neutral",
            feedback_stage="chat",
            data="Optional"
        )

    Note:
        - This class is used to represent feedback data with a specified `feedback_id`.
        - It is typically used when retrieving or working with existing feedback data.
    """
    
    feedback_id: str 
    
    class Config:
        from_attibutes = True
        json_schema_extra = {
            "examples": [
                {
                    "feedback_id": uuid.uuid4(),
                    "created_at": datetime.utcnow(),
                    "session_id": "98766545431",
                    "feedback": 1,
                    "feedback_stage": "chat",
                    "data": "Optional"
                }
            ]
        }

class TicketBase(BaseModel):
    """
    Base model for tickets.

    This class defines a base data model for tickets, including attributes such as the
    ticket creation timestamp, session ID, and additional data.

    Attributes:
        - created_at (Optional[datetime]): The timestamp when the ticket was created.
          Default is the current UTC time.
        - session_id (Optional[str]): The session ID associated with the ticket. Default
          is None.
        - data (Optional[str]): Additional data related to the ticket. Default is None.

    Example Usage:
        # Creating an instance of TicketBase with sample data
        ticket_data = TicketBase(
            created_at=datetime.utcnow(),
            session_id="98766545431",
            data="Optional"
        )

    Note:
        - This class serves as a base model for ticket data, and its attributes can be
          optional to accommodate various use cases.
    """
    
    
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None
    data: Optional[str] = None
    
class TicketCreate(TicketBase):
    """
    Model for creating a ticket.

    This class extends the base `TicketBase` model and adds an attribute for the
    `ticket_id`, which represents a unique identifier for the ticket being created.

    Attributes:
        - ticket_id (Optional[str]): A unique identifier for the ticket. It is generated
          using the `generate_id` function by default.

    Example Usage:
        # Creating an instance of TicketCreate with sample data
        ticket_data = TicketCreate(
            ticket_id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            session_id="98766545431",
            data="Optional"
        )

    Note:
        - This class is used to represent ticket data when creating new tickets, and it
          includes additional attributes beyond the base `TicketBase`.
    """
    
    
    ticket_id: Optional[str] = Field(default_factory=generate_id)
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "ticket_id": uuid.uuid4(),
                    "created_at": datetime.utcnow(),
                    "session_id": "98766545431",
                    "data": "Optional"
                }
            ]
        }

class Ticket(TicketBase):
    """
    Model representing a ticket.

    This class extends the base `TicketBase` model and includes an attribute for the
    `ticket_id`, which represents a unique identifier for the ticket.

    Attributes:
        - ticket_id (str): A unique identifier for the ticket.

    Example Usage:
        # Creating an instance of Ticket with sample data
        ticket_data = Ticket(
            ticket_id=str(uuid.uuid4()),
            created_at=datetime.utcnow(),
            session_id="98766545431",
            data="Optional"
        )

    Note:
        - This class is used to represent ticket data with a specified `ticket_id`.
        - It is typically used when retrieving or working with existing ticket data.
    """
    
    
    ticket_id: str
    
    class Config:
        from_attibutes = True
        json_schema_extra = {
            "examples": [
                {
                    "ticket_id": uuid.uuid4(),
                    "created_at": datetime.utcnow(),
                    "session_id": "98766545431",
                    "data": "Optional"
                }
            ]
        }