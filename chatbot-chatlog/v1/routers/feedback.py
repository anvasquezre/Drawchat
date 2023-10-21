
# Import FastAPI framework

from fastapi import APIRouter, Depends, HTTPException
from typing import List

# Import PyMongo framework
from pymongo import MongoClient

# Import the Feedback model and the FeedbackCreate Pydantic model from core.models
from core.models.models import (
    Feedback as FeedbackModel,
    FeedbackCreate,
)

# Import the settings from core.settings
from core.settings import settings

# Import the get_client_uri function from utils.utils
from v1.utils.utils import get_client


# Create a router instance for the Feedback Logging API
router = APIRouter(prefix="/feedback",
    tags=["Feedback Logging"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=FeedbackModel)
def create_feedback(
    feedback: FeedbackCreate,
    client: MongoClient = Depends(get_client)
    ) -> FeedbackModel: 
    """
    Create a new feedback record in the database.

    This endpoint allows you to create a new feedback record by providing the necessary
    data in the request body. The feedback data will be inserted into the database
    and a response containing the newly created feedback will be returned.

    Parameters:
        - feedback (FeedbackCreate): The feedback data to be created.
        - client (MongoClient, optional): An optional MongoDB client obtained from the
        dependency injection. If not provided, a new client will be created.

    Returns:
        FeedbackModel: A response model containing the newly created feedback data.

    Raises:
        HTTPException (status_code=500): If an error occurs while inserting the feedback
        data into the database, an internal server error is raised, and the error details
        are provided in the response.
        
        HTTPException (status_code=404): If the feedback data could not be found in the
        database, a not found error is raised, and the error details are provided in the
        response.
    
    Note:
        - The database operation is performed within a transactional session to ensure
          atomicity and consistency.
        - If a new MongoDB client is created, it will be automatically closed after
          processing the request.
        - The MongoDB collection used for storing feedback data is specified in the
          application settings (settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK).
    """
    
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    # Starting a session to ensure atomicity and consistency
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK]
        try:
            # Inserting the data into the collection
            collection.insert_one(feedback.model_dump(),session=session)
            return FeedbackModel(**feedback.model_dump())
        except Exception as e:
            print(e)
            print("Couldn't insert into database")
            raise HTTPException(status_code=500, detail="Internal Server Error")
            
    
@router.get("/{feedback_id}", response_model=FeedbackModel)
def read_feedback(
    feedback_id: str, 
    client: MongoClient = Depends(get_client)
    ) -> FeedbackModel:
    """
    Retrieve a feedback record by its unique identifier.

    This endpoint allows you to retrieve a feedback record from the database by providing
    its unique identifier (`feedback_id`) as a path parameter. The specified feedback record
    will be retrieved from the database using a MongoDB client, and a response containing
    the retrieved feedback data will be returned.

    Parameters:
        - feedback_id (str): The unique identifier of the feedback record to retrieve.
        - client (MongoClient, optional): An optional MongoDB client obtained from the
          dependency injection. If not provided, a new client will be created.

    Returns:
        FeedbackModel: A response model containing the retrieved feedback data.

    Raises:
        HTTPException (status_code=400): If the `feedback_id` parameter is invalid or
        the request is malformed, a bad request error is raised, and the error details
        are provided in the response.

        HTTPException (status_code=404): If the specified feedback record is not found
        in the database, a not found error is raised, and the error details are provided
        in the response.

        HTTPException (status_code=500): If an unexpected server error occurs while
        querying the database, an internal server error is raised, and the error details
        are provided in the response.

    Note:
        - The database query is performed within a transactional session to ensure
          atomicity and consistency.
        - If a new MongoDB client is created, it will be automatically closed after
          processing the request.
        - The MongoDB collection used for storing feedback data is specified in the
          application settings (settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK).
    """
    # Get the MongoDB database and collection
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK]
        # Query the database for the feedback record
        try:
            db_feedback = collection.find_one({"feedback_id": feedback_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            # If the feedback record is not found, raise a not found error
            if db_feedback is None:
                raise HTTPException(status_code=404, detail="Feedback not found")
            # Return the retrieved feedback record
            return FeedbackModel(**db_feedback)

@router.put("/{feedback_id}", response_model=FeedbackModel)
def update_feedback(
    feedback_id: str, 
    message: FeedbackCreate,
    client: MongoClient = Depends(get_client)
    ) -> FeedbackModel:
    """
    Update an existing feedback record in the database.

    This endpoint allows you to update an existing feedback record in the database by
    providing its unique identifier (`feedback_id`) as a path parameter and the updated
    feedback data in the request body (`message`). The specified feedback record will be
    retrieved from the database, and the provided updates will be applied. The updated
    feedback data will then be saved to the database, and a response containing the
    updated feedback will be returned.

    Parameters:
        - feedback_id (str): The unique identifier of the feedback record to update.
        - message (FeedbackCreate): The updated feedback data to be applied.
        - client (MongoClient, optional): An optional MongoDB client obtained from the
          dependency injection. If not provided, a new client will be created.

    Returns:
        FeedbackModel: A response model containing the updated feedback data.

    Raises:
        HTTPException (status_code=400): If the `feedback_id` parameter is invalid, the
        request data is invalid, or the request is malformed, a bad request error is
        raised, and the error details are provided in the response.

        HTTPException (status_code=404): If the specified feedback record is not found
        in the database, a not found error is raised, and the error details are provided
        in the response.

        HTTPException (status_code=500): If an unexpected server error occurs while
        querying or updating the database, an internal server error is raised, and the
        error details are provided in the response.

    Note:
        - The database query and update operations are performed within a transactional
          session to ensure atomicity and consistency.
        - If a new MongoDB client is created, it will be automatically closed after
          processing the request.
        - The MongoDB collection used for storing feedback data is specified in the
          application settings (settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK).
    """
    # Get the MongoDB database and collection
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK]
        try:
            db_feedback = collection.find_one({"feedback_id": feedback_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            # If the feedback record is not found, raise a not found error
            if db_feedback is None:
                raise HTTPException(status_code=404, detail="Feedback not found")
            # Create a new FeedbackModel instance with the updated data
            data = FeedbackModel(**db_feedback)
            update_data = message.model_dump(exclude_unset=True)
            # Update the feedback record with the new data
            for key, value in update_data.items():
                setattr(data, key, value)
            # Save the updated feedback record to the database
            try:
                collection.update_one({"feedback_id": feedback_id}, {"$set": data.model_dump()},session=session)
                return data
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{feedback_id}", response_model=FeedbackModel)
def delete_feedback(
    feedback_id: str, 
    client: MongoClient = Depends(get_client), 
    ) -> FeedbackModel:
    """
    Delete an existing feedback record from the database.

    This endpoint allows you to delete an existing feedback record from the database by
    providing its unique identifier (`feedback_id`) as a path parameter. The specified
    feedback record will be retrieved from the database and then deleted. A response
    containing the deleted feedback data will be returned.

    Parameters:
        - feedback_id (str): The unique identifier of the feedback record to delete.
        - client (MongoClient, optional): An optional MongoDB client obtained from the
          dependency injection. If not provided, a new client will be created.

    Returns:
        FeedbackModel: A response model containing the deleted feedback data.

    Raises:
        HTTPException (status_code=400): If the `feedback_id` parameter is invalid,
        the request data is invalid, or the request is malformed, a bad request error is
        raised, and the error details are provided in the response.

        HTTPException (status_code=404): If the specified feedback record is not found
        in the database, a not found error is raised, and the error details are provided
        in the response.

        HTTPException (status_code=500): If an unexpected server error occurs while
        querying or deleting the database record, an internal server error is raised, and
        the error details are provided in the response.

    Note:
        - The database query and delete operations are performed within a transactional
          session to ensure atomicity and consistency.
        - If a new MongoDB client is created, it will be automatically closed after
          processing the request.
        - The MongoDB collection used for storing feedback data is specified in the
          application settings (settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK).
    """
    # Get the MongoDB database and collection
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK]
        # Query the database for the feedback record
        try:
            db_feedback = collection.find_one({"feedback_id": feedback_id},session=session)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            if db_feedback is None:
                raise HTTPException(status_code=404, detail="Feedback not found")
            # Delete the feedback record from the database
            try:
                collection.delete_one({"feedback_id": feedback_id},session=session)
                return FeedbackModel(**db_feedback)
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

# List feedbacks
@router.get("/", response_model=List[FeedbackModel])
def list_feedbacks(
    skip: int = 0,
    limit: int = 10, 
    client: MongoClient = Depends(get_client) 
    ) -> List[FeedbackModel]:
    """
    List feedback records from the database.

    This endpoint allows you to retrieve a list of feedback records from the database
    with optional pagination parameters (`skip` and `limit`). The retrieved feedback
    records are returned as a list of `FeedbackModel` objects in the response.

    Parameters:
        - skip (int, optional): The number of records to skip before starting to return
          feedback records. Default is 0.
        - limit (int, optional): The maximum number of feedback records to return in the
          response. Default is 10.
        - client (MongoClient, optional): An optional MongoDB client obtained from the
          dependency injection. If not provided, a new client will be created.

    Returns:
        List[FeedbackModel]: A list of `FeedbackModel` objects containing the retrieved
        feedback records.

    Raises:
        HTTPException (status_code=400): If the `skip` or `limit` parameters are invalid
        or the request is malformed, a bad request error is raised, and the error details
        are provided in the response.

        HTTPException (status_code=404): If no feedback records are found in the database
        based on the specified `skip` and `limit` parameters, a not found error is raised,
        and the error details are provided in the response.

        HTTPException (status_code=500): If an unexpected server error occurs while
        querying the database, an internal server error is raised, and the error details
        are provided in the response.

    Note:
        - The database query is performed within a transactional session to ensure
          atomicity and consistency.
        - If a new MongoDB client is created, it will be automatically closed after
          processing the request.
        - The MongoDB collection used for storing feedback data is specified in the
          application settings (settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK).
    """
    # Get the MongoDB database and collection
    db = client[settings.db.MONGO_CHATLOG_DB_NAME]
    with client.start_session(causal_consistency=True) as session:
        collection = db[settings.db.MONGO_CHATLOG_COLLECTION_FEEDBACK]
        # Query the database for the feedback records
        try:
            messages_cursor = collection.find(session=session).skip(skip).limit(limit)
            messages = [FeedbackModel(**message) for message in messages_cursor]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            # If no feedback records are found, raise a not found error
            if not messages:
                raise HTTPException(status_code=404, detail="Feedbacks not found")
            # Return the retrieved feedback records
            return messages
    