import os
import typing
from importlib import import_module
from fastapi import HTTPException
import numpy as np
import settings

def create_file(suffix_name: str, content: typing.Union[str,typing.List[str]]):
    """
    Description:
        Create a file python file using the content.
    """
    with open( os.path.join( settings.LOCAL_FILE_STORAGE, f'{suffix_name}.py'),'w') as python_file:
        for item in content:
            python_file.write(item)

def transform_values_dict(data_obj: dict) -> dict:
    """
    Description:
        In nested dictionaries convert the numpy arrays in python list.
    """
    if isinstance(data_obj, np.ndarray):
        return list(data_obj)

    if isinstance(data_obj, dict):
        for key, value in data_obj.items():
            data_obj.update({key: transform_values_dict(value)})
    elif isinstance(data_obj,list):
        return [transform_values_dict(item) for item in data_obj]
    return data_obj

def get_method_by_local_file(file_name:str, method:str) -> typing.Callable:
    """
    Description:
        Import a local file during the execution.
    Arguments:
        - file_name: string that represents the name of the file.
        - method: string that represent the function or variable to find in
            the file.
    """
    try:
        module = import_module(f'{settings.LOCAL_FILE_STORAGE}.{file_name}')
        return getattr(module, method)
    except Exception as error:
        raise HTTPException(    
            status_code= 404,
            detail= str(error)
        )