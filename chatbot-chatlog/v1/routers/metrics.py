
from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from pymongo import MongoClient

from v1.utils.utils import get_client
from v1.utils.metric_utils import (
    FUNC_MAPPING
)

# Create the router instance for the metrics endpoint
router = APIRouter(prefix="/metrics",
    tags=["Metrics Estimation"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{metric_type}")
async def read_metric(
    metric_type: str, 
    client: MongoClient = Depends(get_client)
    ) -> Any:
    """
    Read a specific metric data.

    This endpoint allows reading a specific metric's data based on the provided metric_type.
    The metric_type should match one of the keys in the FUNC_MAPPING dictionary, which maps
    metric types to corresponding async functions for data retrieval.

    Args:
        - metric_type (str): The type of metric to retrieve (e.g., "messages", "sessions").
        - client (MongoClient, optional): The MongoDB client obtained from the dependency
          `get_client`. Defaults to None.

    Returns:
        - dict: The metric data, typically hourly values.

    Raises:
        - HTTPException 404: If the provided metric_type does not match any known metrics
          in FUNC_MAPPING, it raises an HTTPException with a status code of 404 (Not Found).

    Example Usage:
        GET /metrics/messages

    Notes:
        - This endpoint retrieves metric data based on the specified metric_type.
        - The FUNC_MAPPING dictionary maps metric types to corresponding async functions
          responsible for data retrieval.
        - If the metric_type is not found in FUNC_MAPPING, it raises a 404 status code.
    """
    
    # Check if the metric_type is valid
    if metric_type not in FUNC_MAPPING.keys():
        # If not, raise an HTTPException with a 404 status code
        raise HTTPException(status_code=404, detail="Metric not found")
    # If the metric_type is valid, retrieve the corresponding async function
    func = FUNC_MAPPING[metric_type]
    # Call the async function to retrieve the metric data
    daily_values = await func(client)
    # Return the metric data
    return daily_values

