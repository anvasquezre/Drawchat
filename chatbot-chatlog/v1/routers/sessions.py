from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pymongo import MongoClient

# Import the models from the models folder
from core.models.models import (
    Message as MessageModel,
    Session as SessionModel,
    SessionCreate,
)
# Import the settings from the core folder
from core.settings import settings

# Import the get_client dependency from the utils folder
from v1.utils.utils import get_client


# Create the router instance for the sessions endpoint
router = APIRouter(prefix="/sessions",
    tags=["Sessions Logging"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=SessionModel)
def create_session(
    session_data: SessionCreate,
    client: MongoClient = Depends(get_client)
    ) -> SessionModel: 
    """
    Create a new session.

    This endpoint allows the creation of a new session. It inserts the session data
    into the database collection specified in the settings.

    Args:
        - session_data (SessionCreate): The session data to be created.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - SessionModel: The created session.

    Raises:
        - HTTPException: If there is an issue with inserting the data into the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        POST /sessions/
        {
            "session_id": "abcdef12345",
            "created_at": "2023-09-22T12:34:56.789Z",
            "ended_at": null,
            "user_email": "user@email.com",
            "user_name": "John Doe",
            "user_role": "Owner/Applicant/Realtor",
            "data_user_consent": true,
            "metadata": {
                "ip": "111.111.11.111",
                "device": "Mobile/Desktop",
                "browser": "Chrome",
                "os": "Windows/Linux/MacOS"
            }
        }
    """
    
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    # Starting a session to ensure atomicity and consistency
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_SESSIONS]
        try:
            # Inserting the data into the collection
            collection.insert_one(session_data.model_dump(),session=session)
            return SessionModel(**session_data.model_dump())
        except Exception as e:
            print(e)
            print("Couldn't insert into database")
            raise HTTPException(status_code=500, detail="Internal Server Error")
            
    
@router.get("/{session_id}", response_model=SessionModel)
def read_session(
    session_id: str, 
    client: MongoClient = Depends(get_client)
    ) -> SessionModel:
    """
    Read a session.

    This endpoint allows reading a specific session's data based on the provided session_id.

    Args:
        - session_id (str): The ID of the session to retrieve.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - SessionModel: The retrieved session.

    Raises:
        - HTTPException 404: If the specified session_id does not exist in the database,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with retrieving the data from the
          database, it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        GET /sessions/abcdef12345
    """
    
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_SESSIONS]
        try:
            db_session = collection.find_one({"session_id": session_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_session is None:
                raise HTTPException(status_code=404, detail="Session not found")
            return SessionModel(**db_session)

@router.put("/{session_id}", response_model=SessionModel)
def update_session(
    session_id: str, 
    session_data: SessionCreate,
    client: MongoClient = Depends(get_client)
    ) -> SessionModel:
    """
    Update a session.

    This endpoint allows updating a specific session's data based on the provided session_id.

    Args:
        - session_id (str): The ID of the session to update.
        - session_data (SessionCreate): The updated session data.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - SessionModel: The updated session.

    Raises:
        - HTTPException 404: If the specified session_id does not exist in the database,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with updating the data in the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        PUT /sessions/abcdef12345
        {
            "session_id": "abcdef12345",
            "created_at": "2023-09-22T12:34:56.789Z",
            "ended_at": "2023-09-22T13:00:00.000Z",
            "user_email": "updated_email@email.com",
            "user_name": "Updated Name",
            "user_role": "Updated Role",
            "data_user_consent": true,
            "metadata": {
                "ip": "111.111.11.111",
                "device": "Mobile/Desktop",
                "browser": "Chrome",
                "os": "Windows/Linux/MacOS"
            }
        }
    """
    
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_SESSIONS]
        try:
            db_session = collection.find_one({"session_id": session_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_session is None:
                raise HTTPException(status_code=404, detail="Session not found")

            data = SessionModel(**db_session)
            update_data = session_data.model_dump(exclude_unset=True)
            
            for key, value in update_data.items():
                setattr(data, key, value)

            try:
                collection.update_one({"session_id": session_id}, {"$set": data.model_dump()},session=session)
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{session_id}", response_model=SessionModel)
def delete_session(
    session_id: str, 
    client: MongoClient = Depends(get_client), 
    ) -> SessionModel:
    """
    Delete a session.

    This endpoint allows deleting a specific session based on the provided session_id.

    Args:
        - session_id (str): The ID of the session to delete.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - SessionModel: The deleted session.

    Raises:
        - HTTPException 404: If the specified session_id does not exist in the database,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with deleting the data from the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        DELETE /sessions/abcdef12345
    """
    
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_SESSIONS]
        try:
            db_session = collection.find_one({"session_id": session_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_session is None:
                raise HTTPException(status_code=404, detail="Session not found")

            try:
                collection.delete_one({"session_id": session_id},session=session)
                return SessionModel(**db_session)
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

# List all sessions
@router.get("/", response_model=List[SessionModel])
def list_sessions(
    skip: int = 0,
    limit: int = 10, 
    client: MongoClient = Depends(get_client) 
    ) -> List[SessionModel]:
    """
    List all sessions.

    This endpoint allows listing all sessions with optional pagination.

    Args:
        - skip (int, optional): The number of sessions to skip. Defaults to 0.
        - limit (int, optional): The maximum number of sessions to retrieve. Defaults to 10.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - List[SessionModel]: A list of sessions.

    Raises:
        - HTTPException 404: If there are no sessions found, it raises an HTTPException
          with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with retrieving the data from the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        GET /sessions/?skip=0&limit=10
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_SESSIONS]
        try:
            sessions_cursor = collection.find(session=session).skip(skip).limit(limit)
            sessions = [SessionModel(**session_found) for session_found in sessions_cursor]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not sessions:
                raise HTTPException(status_code=404, detail="Sessions not found")
            return sessions

# Endpoint to retrieve all sessions from a single session
@router.get("/{session_id}/messages/", response_model=List[MessageModel])
def get_messages_for_session(
    session_id: str,
    client: MongoClient = Depends(get_client) 
    ) -> List[MessageModel]:
    """
    Get messages for a session.

    This endpoint allows retrieving messages associated with a specific session based
    on the provided session_id.

    Args:
        - session_id (str): The ID of the session to retrieve messages for.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - List[MessageModel]: A list of messages associated with the session.

    Raises:
        - HTTPException 404: If there are no messages found for the session, it raises
          an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with retrieving the data from the
          database, it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        GET /sessions/abcdef12345/messages/
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_MESSAGES]
        try:
            messages_cursor = collection.find({"session_id": session_id},session=session).limit(0)
            messages = [MessageModel(**message) for message in messages_cursor]
        except HTTPException as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not messages:
                raise HTTPException(status_code=404, detail="No messages found for this session")
            return messages