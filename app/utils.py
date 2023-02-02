import os
import typing
import logging
from importlib import import_module, reload
import numpy as np
import settings


class ModulesHandler:
    """
    Helper class to save the most recent python script in memory.
    """

    modules = {}

    @classmethod
    def upload_module(cls, module_name: str) -> None:
        """
        Description:
            This method saves the most recent information in the files uploaded.
        """
        if module_name in cls.modules:
            cls.modules[module_name] = reload(cls.modules[module_name])
        else:
            cls.modules[module_name] = import_module(
                f"{settings.LOCAL_FILE_STORAGE}.{module_name}"
            )

    @classmethod
    def get_method_by_module(cls, module_name: str, method: str) -> typing.Callable:
        """
        Description:
            Import a local file during the execution.
        Arguments:
            - module_name: string that represents the name of the python file.
            - method: string that represent the function or variable to find in
                the file.
        """
        return getattr(cls.modules[module_name], method)


def create_file(suffix_name: str, content: typing.Union[str, typing.List[str]]):
    """
    Description:
        Create a file python file using the content.
    """
    with open(
        os.path.join(settings.LOCAL_FILE_STORAGE, f"{suffix_name}.py"),
        "w",
        encoding="utf-8",
    ) as python_file:
        for item in content:
            python_file.write(item)
    ModulesHandler().upload_module(suffix_name)


def transform_values_dict(data_obj: dict) -> dict:
    """
    Description:
        In nested dictionaries convert the numpy arrays in python list.
    """

    if isinstance(data_obj, dict):
        for key, value in data_obj.items():
            data_obj.update({key: transform_values_dict(value)})

    elif isinstance(data_obj, np.ndarray):
        return list(data_obj.astype(float))

    elif isinstance(data_obj, list):
        return [transform_values_dict(item) for item in data_obj]

    return data_obj


def create_logger(file_name:str):
    """
    Description:
        Creates a logging object.
    Arguments:
        - logger_name: string that helps us to recognize the logger.
        - file_name: string that indicates the file name where to save the logs.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s: %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
    )
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
