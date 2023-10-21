
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pymongo import MongoClient

# Import the Ticket model and TicketCreate model from core.models.models
from core.models.models import (
    Ticket as TicketModel,
    TicketCreate,
)
# Import the settings from the core.settings module
from core.settings import settings

# Import the get_client dependency from utils
from v1.utils.utils import get_client


# Create the router instance for the tickets endpoint
router = APIRouter(
    prefix="/tickets",
    tags=["Ticket Logging"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=TicketModel)
def create_ticket(
    ticket: TicketCreate,
    client: MongoClient = Depends(get_client)
    ) -> TicketModel: 
    """
    Create a new ticket.

    This endpoint allows creating a new ticket with the provided ticket data.

    Args:
        - ticket (TicketCreate): The ticket data to create a new ticket.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - TicketModel: The created ticket.

    Raises:
        - HTTPException 500: If there is an issue with inserting the data into the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        POST /tickets/
        Body:
        {
            "ticket_id": "abcdef12345",
            "created_at": "2023-09-22T12:00:00",
            "session_id": "98766545431",
            "data": "Optional"
        }
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    # Starting a session to ensure atomicity and consistency
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_TICKETS]
        try:
            # Inserting the data into the collection
            collection.insert_one(ticket.model_dump(),session=session)
            return TicketModel(**ticket.model_dump())
        except Exception as e:
            print(e)
            print("Couldn't insert into database")
            raise HTTPException(status_code=500, detail="Internal Server Error")
            
    
@router.get("/{ticket_id}", response_model=TicketModel)
def read_ticket(
    ticket_id: str, 
    client: MongoClient = Depends(get_client)
    ) -> TicketModel:
    """
    Get a ticket by ID.

    This endpoint allows retrieving a specific ticket based on the provided ticket_id.

    Args:
        - ticket_id (str): The ID of the ticket to retrieve.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - TicketModel: The retrieved ticket.

    Raises:
        - HTTPException 404: If the specified ticket_id does not exist in the database,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with retrieving the data from the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        GET /tickets/abcdef12345
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_TICKETS]
        try:
            db_ticket = collection.find_one({"ticket_id": ticket_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_ticket is None:
                raise HTTPException(status_code=404, detail="Ticket not found")
            return TicketModel(**db_ticket)

@router.put("/{ticket_id}", response_model=TicketModel)
def update_ticket(
    ticket_id: str, 
    message: TicketCreate,
    client: MongoClient = Depends(get_client)
    ) -> TicketModel:
    """
    Update a ticket.

    This endpoint allows updating a specific ticket based on the provided ticket_id.

    Args:
        - ticket_id (str): The ID of the ticket to update.
        - ticket_data (TicketCreate): The updated ticket data.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - TicketModel: The updated ticket.

    Raises:
        - HTTPException 404: If the specified ticket_id does not exist in the database,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with updating the data in the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        PUT /tickets/abcdef12345
        Body:
        {
            "created_at": "2023-09-22T13:00:00",
            "session_id": "98766545431",
            "data": "Updated data"
        }
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_TICKETS]
        try:
            db_ticket = collection.find_one({"ticket_id": ticket_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_ticket is None:
                raise HTTPException(status_code=404, detail="Ticket not found")

            data = TicketModel(**db_ticket)
            update_data = message.model_dump(exclude_unset=True)
            
            for key, value in update_data.items():
                setattr(data, key, value)

            try:
                collection.update_one({"ticket_id": ticket_id}, {"$set": data.model_dump()},session=session)
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{ticket_id}", response_model=TicketModel)
def delete_ticket(
    ticket_id: str, 
    client: MongoClient = Depends(get_client), 
    ) -> TicketModel:
    """
    Delete a ticket.

    This endpoint allows deleting a specific ticket based on the provided ticket_id.

    Args:
        - ticket_id (str): The ID of the ticket to delete.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - TicketModel: The deleted ticket.

    Raises:
        - HTTPException 404: If the specified ticket_id does not exist in the database,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with deleting the data from the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        DELETE /tickets/abcdef12345
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_TICKETS]
        try:
            db_ticket = collection.find_one({"ticket_id": ticket_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_ticket is None:
                raise HTTPException(status_code=404, detail="Ticket not found")

            try:
                collection.delete_one({"ticket_id": ticket_id},session=session)
                return TicketModel(**db_ticket)
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

# List tickets
@router.get("/", response_model=List[TicketModel])
def list_tickets(
    skip: int = 0,
    limit: int = 10, 
    client: MongoClient = Depends(get_client) 
    ) -> List[TicketModel]:
    """
    List all tickets.

    This endpoint allows listing all the tickets in the database with optional pagination.

    Args:
        - skip (int, optional): The number of tickets to skip before returning results. Defaults to 0.
        - limit (int, optional): The maximum number of tickets to return. Defaults to 10.
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - List[TicketModel]: A list of tickets.

    Raises:
        - HTTPException 404: If there are no tickets found in the database,
          it raises an HTTPException with a status code of 404 (Not Found).
        - HTTPException 500: If there is an issue with retrieving the data from the database,
          it raises an HTTPException with a status code of 500 (Internal Server Error).

    Example Usage:
        GET /tickets/
    """
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_TICKETS]
        try:
            messages_cursor = collection.find(session=session).skip(skip).limit(limit)
            messages = [TicketModel(**message) for message in messages_cursor]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if not messages:
                raise HTTPException(status_code=404, detail="Tickets not found")
            return messages
    