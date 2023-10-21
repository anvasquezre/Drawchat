from fastapi import FastAPI
from v1 import app


api = FastAPI(docs_url="/documentation", redoc_url="/redocumentation")

api.include_router(app.router, include_in_schema=True)

