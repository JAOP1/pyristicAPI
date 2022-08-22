from enum import Enum
import pydantic
import typing

class EvolutionaryOperatorConfig(pydantic.BaseModel):
    """
    Operator for our evolutionary algorithm.
    """
    operator_name:str
    parameters:typing.Union[typing.List[float], typing.List[typing.List[float]]]

class EvolutionaryOperators(pydantic.BaseModel):
    """
    Dictionary where every key is a required method for our evolutionary
    metaheuristic.
    """
    methods: typing.Dict[str,EvolutionaryOperatorConfig]

class OptimizerArguments(pydantic.BaseModel):
    """
    Arguments for the optimize method in the metaheuristic.
    """
    arguments: typing.Dict[str,float]

class EvolutionaryAlgorithm(str, Enum):
    """
    Constraint the types accepted as route entry.
    """
    GA = "GA"
    EP = "EP"
    EE = "EE"

class FileType(str,Enum):
    """
    Constraint the types accepted as file name.
    """
    FUNCTION = 'function'
    CONSTRAINTS = 'constraints'
    SEARCH_SPACE = 'search_space'

class StringInput(pydantic.BaseModel):
    """
    Content type.
    """
    content: typing.Union[str, typing.List[str]]
