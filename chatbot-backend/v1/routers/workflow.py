
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Request
from core.models.graph_model import Root
# Import the settings from the core.settings module
from core.settings import settings
import json
import os
import tempfile
# Import the get_client dependency from utils


# Create the router instance for the tickets endpoint
router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"],
    responses={404: {"description": "Not found"}}
)

@router.post("/publish")
def create_production(
    request:Root,
    ): 

    try:
        # Inserting the data into the collection
        # TODO set ENV variables for paths
        json_path = str(Path(__file__).parent.parent / 'src/flows/flow_production.json')
        if os.path.exists(json_path):
            os.remove(json_path)
        flow = request.model_dump_json(indent=4)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                flow = request.model_dump_json(indent=4 , by_alias=True)
                temp_file.write(flow)

            # Replace the original file with the temporary one
        os.replace(temp_file.name, json_path)
    except Exception as e:
        print(e)
        print("Couldn't Save Flow")
        raise HTTPException(status_code=500, detail="Internal Server Error")
            
@router.get("/fetch/{type}")
def get_latest(type:str = "prod"):
    file = "flow_production.json" if type == "prod" else "flow_latest.json"
    
    json_path = str(Path(__file__).parent.parent / 'src/flows/{file}'.format(file=file))
    with open(json_path, 'r') as f:
        data = f.read()
    data = json.loads(data)
    workflow = Root(**data)
    return workflow


@router.post("/autosave")
def autosave(request: Root):
    try:
        # Inserting the data into the collection
        # TODO set ENV variables for paths
        json_path = str(Path(__file__).parent.parent / 'src/flows/flow_latest.json')
        if os.path.exists(json_path):
            os.remove(json_path)
            
        flow = request.model_dump_json(indent=4)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                flow = request.model_dump_json(indent=4, by_alias=True)
                temp_file.write(flow)

            # Replace the original file with the temporary one
        os.replace(temp_file.name, json_path)
    except Exception as e:
        print(e)
        print("Couldn't Save Flow")
        raise HTTPException(status_code=500, detail="Internal Server Error")
