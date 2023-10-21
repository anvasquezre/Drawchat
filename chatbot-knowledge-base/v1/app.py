from fastapi import APIRouter, Depends
import json

# Import the routers from the v1 folder
from v1.routers import (
    generate,
    knowledge_base
)

# Import the has_access dependency from utils
from v1.utils.utils import has_access


# Define the PROTECTED dependency to protect the endpoints
# PROTECTED = [Depends(has_access)]

# Create the router instance for the API
router = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
   # dependencies=PROTECTED
)

# List of all the routers
routes = [
    knowledge_base.router,
    generate.router
]
# Include all the routers in the API
for route in routes:
    router.include_router(route)

# Define the root endpoint
@router.get("/")
async def read_items():
    message = {"version":"API v1.0.1"}
    return json.dumps(message)