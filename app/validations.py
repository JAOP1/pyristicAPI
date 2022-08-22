"""
Validations applied to the heuristic routes.
"""
import os
import typing
from fastapi import HTTPException
from .settings import ROOT_PATH, LOCAL_FILE_STORAGE

class ValidateFiles:
    """
    Description:
        required this format to keep validate_required_files for general
        porpouse.
    """
    def __init__(self, file_list: typing.List[str]):
        self.files = file_list
    
    def __call__(self):
        validate_required_files(self.files)

def validate_required_files(files: typing.List[str])->bool:
    """
    Description:
        Check if the required files exist.
    Arguments:
        -None.
    """
    for file in files:
        file_path = os.path.join( ROOT_PATH, LOCAL_FILE_STORAGE, f'{file}.py')
        if not os.path.exists(file_path):
            raise HTTPException(
                    status_code= 404,
                    detail= f"The file called {file}.py not found."
                )
