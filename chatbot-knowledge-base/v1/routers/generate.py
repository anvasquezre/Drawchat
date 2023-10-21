
# Import FastAPI framework
from fastapi import APIRouter, Depends, HTTPException
# Import the Feedback model and the FeedbackCreate Pydantic model from core.models
from core.models.models import (
    GenerateQuery,
    GenerateResponse
)
from v1.src.chains import create_chain


from langchain.schema import Document
# Create a router instance for the Feedback Logging API
router = APIRouter(prefix="/generate",
    tags=["Generate API"],
    responses={404: {"description": "Not found"}}
)


    
@router.post("/", response_model=GenerateResponse)
def generate_ai(
    query: GenerateQuery
    ) -> GenerateResponse:

    try:
        model_kwargs = query.llm_model_kwargs.model_dump()
        model = query.model
        system_prompt = query.system_prompt
        print(system_prompt)
        if not query.human_prompt:
            raise HTTPException(
                status_code=500,
                detail="No message found")
        gen_query = query.human_prompt
        llm_model = create_chain(model=model, model_kwargs=model_kwargs, human_message_prompt="{query}", system_message_prompt=system_prompt)
        answer = llm_model({"query" : gen_query})["text"]
        
        return GenerateResponse(
            answer=answer,
            **query.model_dump(),
            )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e))
        