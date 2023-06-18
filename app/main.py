"""Initialization of the API instance."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.generic import create_logger
from app.constants import OAPI_TAGS, LOGS_FILE
from app.routes.heuristic_routes import heuristics_router
from app.routes.utilities_routes import utilities_router

app = FastAPI(
    title="pyristic-api",
    description=(
        "API to create files related to the optimization"
        "problem and perform one of the search algorithm that has pyristic."
    ),
    docs_url="/",
    openapi_tags=OAPI_TAGS,
)

app.include_router(heuristics_router)
app.include_router(utilities_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOGGER = create_logger(LOGS_FILE)
