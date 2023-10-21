
# Import FastAPI framework
from fastapi import APIRouter, Depends, HTTPException
from qdrant_client import QdrantClient
# Import the Feedback model and the FeedbackCreate Pydantic model from core.models
from core.models.models import (
    DocumentQuery,
    DocumentQueyResponse,
    UpdateQuery,
    UpdateResponse,
    DocumentListDTO,
    DocumentDTO
)
from langchain.vectorstores import Qdrant
# Import the settings from core.settings
from core.settings import settings
# Import the get_client_uri function from utils.utils
from v1.utils.utils import get_client
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
from v1.src.chains import create_chain
import json

from langchain.schema import Document
# Create a router instance for the Feedback Logging API
router = APIRouter(prefix="/knowledgebase",
    tags=["Knowledgebase API"],
    responses={404: {"description": "Not found"}}
)



embeddings = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v1")
collections_list = settings.qdrant.COLLECTIONS
print("Based Settings Initialized")


router = APIRouter(prefix="/kb",
    tags=["Knowledgebase API"],
    responses={404: {"description": "Not found"}},
)
    
@router.post("/{collection}/query", response_model=DocumentQueyResponse)
def query_db(
    query: DocumentQuery, 
    client: QdrantClient = Depends(get_client),
    collection: str = "faqs"
    ) -> DocumentQueyResponse:

    # Get the MongoDB database and collection
    try:
        if not client:
            raise HTTPException(
                status_code=500,
                detail="No client found")
        if collection not in collections_list:
            raise HTTPException(
                status_code=500,
                detail="Collection not authorized")
        db_index= Qdrant(client=client, collection_name=collection, embeddings=embeddings, distance_strategy="COSINE")
        
        test_query = query.question
        k= query.num_results
        model = query.model
        model_kwargs = query.llm_model_kwargs.model_dump()
        min_score = query.score_threshold
        docs = db_index.similarity_search_with_relevance_scores(test_query,k=k)
        
        docs_text = []
        docs_response = []
        for doc, score in docs:
            page_content = doc.page_content
            answer = doc.metadata["answer"]
            score = score
            if score > min_score: #TODO make this a setting
                docs_text.append(f"{page_content} \n\n {answer}")
                doc_dto = DocumentDTO(page_content=page_content, metadata=doc.metadata, score=score)
                docs_response.append(doc_dto)
        
        context="\n".join(docs_text)
        
        gen_query = { "context": context, "question": test_query}
        
        if query.generate:
            llm_model = create_chain(model=model, model_kwargs=model_kwargs)
            answer = llm_model(gen_query)["text"]
        else:
            answer = None

        retieved_docs = len(docs_response)
        query.num_results = retieved_docs

        return DocumentQueyResponse(
            answer=answer,
            documents=docs_response,
            **query.model_dump(),
            )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e))
        
        
@router.put("/{collection}", response_model=UpdateResponse)
def update_db(
    client: QdrantClient = Depends(get_client),
    collection: str = "faqs",
    ):
    if not client:
        raise HTTPException(
            status_code=500,
            detail="No client found")
    if collection not in collections_list:
        raise HTTPException(
            status_code=500,
            detail="Collection not authorized")
        
    docs = [Document(page_content="test", metadata={"source": "test"})] # Mockup #TODO set this to the actual api call
    try:
        host = settings.qdrant.QDRANT_HOST
        port = int(settings.qdrant.QDRANT_PORT)
        https = settings.qdrant.QDRANT_USE_HTTPS
        grpc_port = int(settings.qdrant.QDRANT_GRPC_PORT)
        db= Qdrant.from_documents(
                            docs,
                            host=host,
                            port=port,
                            https=https,
                            grpc_port=grpc_port,
                            embedding=embeddings,
                           force_recreate=True)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e))
    num_docs = len(docs)
    return UpdateResponse(num_docs=num_docs)


        
@router.post("/{collection}/", response_model=UpdateResponse)
def update_db(
    client: QdrantClient = Depends(get_client),
    collection: str = "faqs",
    documents: DocumentListDTO = None
    ):
    if not client:
        raise HTTPException(
            status_code=500,
            detail="No client found")
           
    if collection not in collections_list:
        raise HTTPException(
            status_code=500,
            detail="Collection not authorized")
        
    doc_list = documents.documents
    docs = [Document(page_content=doc.page_content, metadata=doc.metadata) for doc in doc_list]
    try:
        host = settings.qdrant.QDRANT_HOST
        port = int(settings.qdrant.QDRANT_PORT)
        https = settings.qdrant.QDRANT_USE_HTTPS
        grpc_port = int(settings.qdrant.QDRANT_GRPC_PORT)
        db= Qdrant.from_documents(
                            docs,
                            host=host,
                            port=port,
                            https=https,
                            grpc_port=grpc_port,
                            embedding=embeddings,
                           force_recreate=True)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e))
    num_docs = len(docs)
    return UpdateResponse(num_docs=num_docs)