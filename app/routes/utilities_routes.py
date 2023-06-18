"""Routes that help us to know information about the metaheuristic performed."""
import logging
import traceback
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from app.utils.generic import create_file
from app.constants import LOGS_FILE
from app.models import FileType, StringInput

LOGGER = logging.getLogger(__name__)

utilities_router = APIRouter(
    tags=["Utilities"],
)


@utilities_router.post("/pyristic/connected", status_code=200)
def get_verification_response():
    """Auxiliar function to test the service is working."""
    return JSONResponse(content={"pyristic": "isAlive"})


@utilities_router.get("/logs", status_code=200)
def get_logs():
    """Show logs obtained from the api's."""
    with open(LOGS_FILE, "r", encoding="utf-8") as log_file:
        content = log_file.read()
    return JSONResponse(content={"content": content})


@utilities_router.post("/create-file/{file_name}", status_code=200)
def create_file_request(file_name: FileType, text_content: StringInput):
    """
    Create a file with the content.

    Arguments:
        - file_name: string indicating the file name where to save the content.
        - text_content: string with python code. This content is saved as a python file.
    """
    try:
        create_file(file_name, text_content.content)
        LOGGER.info("Uploaded file %s", file_name)
    except Exception as exc:
        error_detail = traceback.format_exc()
        LOGGER.error(error_detail)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return f"Created with success {file_name}"
