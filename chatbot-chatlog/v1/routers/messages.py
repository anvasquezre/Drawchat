# Import FastAPI
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union
from pymongo import MongoClient

# Add the dependency to other route handlers as needed
# Import the Message model and the MessageCreate model from the models folder
from core.models.models import (
    Message as MessageModel,
    MessageCreate,
)

# Import the settings from the core.settings file
from core.settings import settings

# Import the get_client function from the utils folder
from v1.utils.utils import get_client


# Create the router instance for the messages
router = APIRouter(prefix="/messages",
    tags=["Messages Logging"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=Union[MessageModel, List[MessageModel]])
def create_message(
    message: Union[MessageCreate, List[MessageCreate]],
    client: MongoClient = Depends(get_client)
    ) -> Union[MessageModel, List[MessageModel]]: 
    """
    Create a new chat message.

    This endpoint allows the creation of a new chat message. It inserts the message data
    into the database collection specified in the settings.

    Args:
        - message (MessageCreate): The message data to be created.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - MessageModel: The created chat message.

    Raises:
        - HTTPException: If there is an issue with inserting the data into the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        POST /messages/
        {
            "message_id": "abcdef12345",
            "created_at": "2023-09-22T12:34:56.789Z",
            "exchange": "chat from the user or bot",
            "message_type": "AI/USER",
            "session_id": "98766545431"
        }
    """
    
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    # Starting a session to ensure atomicity and consistency
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        try:
            if isinstance(message, list):
                # Inserting the data into the collection
                collection.insert_many([message.model_dump() for message in message],session=session)
                return [MessageModel(**message.model_dump()) for message in message]
            # Inserting the data into the collection
            collection.insert_one(message.model_dump(),session=session)
            return MessageModel(**message.model_dump())
        except Exception as e:
            print(e)
            print("Couldn't insert into database")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
        
        

            
    
@router.get("/{message_id}", response_model=MessageModel)
def read_message(
    message_id: str, 
    client: MongoClient = Depends(get_client)
    ) -> MessageModel:
    """
    Retrieve a chat message by its ID.

    This endpoint allows retrieving a chat message by its unique identifier (message_id)
    from the database collection specified in the settings.

    Args:
        - message_id (str): The unique identifier of the message to retrieve.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - MessageModel: The retrieved chat message.

    Raises:
        - HTTPException 404: If the message with the given message_id is not found in the
          database, it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with retrieving the data from the
          database, it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        GET /messages/abcdef12345
    """
    
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        try:
            db_message = collection.find_one({"message_id": message_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_message is None:
                raise HTTPException(status_code=404, detail="Message not found")
            return MessageModel(**db_message)

@router.put("/{message_id}", response_model=MessageModel)
def update_message(
    message_id: str, 
    message: MessageCreate,
    client: MongoClient = Depends(get_client)
    ) -> MessageModel:
    
    """
    Update a chat message by its ID.

    This endpoint allows updating a chat message by its unique identifier (message_id) in
    the database collection specified in the settings.

    Args:
        - message_id (str): The unique identifier of the message to update.
        - message (MessageCreate): The updated message data.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - MessageModel: The updated chat message.

    Raises:
        - HTTPException 404: If the message with the given message_id is not found in the
          database, it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with updating the data in the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        PUT /messages/abcdef12345
        {
            "message_id": "abcdef12345",
            "created_at": "2023-09-22T12:34:56.789Z",
            "exchange": "chat from the user or bot",
            "message_type": "AI/USER",
            "session_id": "98766545431"
        }
    """
    
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        try:
            db_message = collection.find_one({"message_id": message_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_message is None:
                raise HTTPException(status_code=404, detail="Message not found")

            data = MessageModel(**db_message)
            update_data = message.model_dump(exclude_unset=True)
            
            for key, value in update_data.items():
                setattr(data, key, value)

            try:
                collection.update_one({"message_id": message_id}, {"$set": data.model_dump()},session=session)
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{message_id}", response_model=MessageModel)
def delete_message(
    message_id: str, 
    client: MongoClient = Depends(get_client), 
    ) -> MessageModel:
    """
    Delete a chat message by its ID.

    This endpoint allows deleting a chat message by its unique identifier (message_id)
    from the database collection specified in the settings.

    Args:
        - message_id (str): The unique identifier of the message to delete.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - MessageModel: The deleted chat message.

    Raises:
        - HTTPException 404: If the message with the given message_id is not found in the
          database, it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with deleting the data from the
          database, it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        DELETE /messages/abcdef12345
    """
    
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        try:
            db_message = collection.find_one({"message_id": message_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_message is None:
                raise HTTPException(status_code=404, detail="Message not found")

            try:
                collection.delete_one({"message_id": message_id},session=session)
                return MessageModel(**db_message)
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

# List all messages
@router.get("/", response_model=List[MessageModel])
def list_messages(
    skip: int = 0,
    limit: int = 10, 
    client: MongoClient = Depends(get_client) 
    ) -> List[MessageModel]:
    """
    List chat messages.

    This endpoint allows listing chat messages with optional pagination (skip and limit).
    It retrieves messages from the database collection specified in the settings.

    Args:
        - skip (int, optional): The number of messages to skip (pagination). Defaults to 0.
        - limit (int, optional): The maximum number of messages to return (pagination).
          Defaults to 10.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - List[MessageModel]: A list of chat messages.

    Raises:
        - HTTPException 404: If no messages are found in the database, it raises an
          HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with retrieving the data from the
          database, it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        GET /messages/?skip=0&limit=10
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        try:
            messages_cursor = collection.find(session=session).skip(skip).limit(limit)
            messages = [MessageModel(**message) for message in messages_cursor]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not messages:
                raise HTTPException(status_code=404, detail="Messages not found")
            return messages
    