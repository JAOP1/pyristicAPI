"""Validations applied to the heuristic routes."""
import os
import typing
from fastapi import HTTPException
from app.constants import LOCAL_FILE_STORAGE


class ValidateFiles:
    """required this format to keep validate_required_files for general porpouse."""

    def __init__(self, file_list: typing.List[str]):
        """
        Keep in memory the expected files to exist.

        Arguments:
            - file_list: the string list that keeps the file names to check.
        """
        self.files = file_list

    def __call__(self):
        """Validate the files are in the expected location."""
        validate_required_files(self.files)


def validate_required_files(files: typing.List[str]) -> bool:
    """
    Check if the required files exist.

    Arguments:
        - files: list of strings to check.
    """
    for file in files:
        file_path = os.path.join(LOCAL_FILE_STORAGE, f"{file}.py")
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, detail=f"The file called {file}.py not found."
            )
