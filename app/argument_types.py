from enum import Enum
import typing
import pydantic

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
    SA_NEIGHBORS = 'SA_neighbor_generator'
    GENERATOR_INITIAL_SOLUTION = 'generator_initial_solution'
    EP_MUTATION_OPERATOR = 'EP_mutation_operator'
    EP_SURVIVOR_SELECTOR = 'EP_survivor_selector'
    EP_SETTER_INVALID_SOLUTION = 'EP_setter_invalid_solution'
    EP_ADAPTIVE_MUTATION_OPERATOR = 'EP_adaptive_mutation_operator'
    EE_MUTATION_OPERATOR = 'EE_mutation_operator'
    EE_SURVIVOR_SELECTOR = 'EE_survivor_selector'
    EE_SETTER_INVALID_SOLUTION = 'EE_setter_invalid_solution'
    EE_ADAPTIVE_CROSSOVER_OPERATOR = 'EE_adaptive_crossover_operator'
    EE_ADAPTIVE_MUTATION_OPERATOR = 'EE_adaptive_mutation_operator'
    EE_CROSSOVER_OPERATOR = 'EE_crossover_operator'
    GA_MUTATION_OPERATOR = 'GA_mutation_operator'
    GA_SURVIVOR_SELECTOR = 'GA_survivor_selector'
    GA_SETTER_INVALID_SOLUTION = 'GA_setter_invalid_solution'
    GA_CROSSOVER_OPERATOR = 'GA_crossover_operator'
    GA_PARENT_SELECTOR = 'GA_parent_selector'


class StringInput(pydantic.BaseModel):
    """
    Content type.
    """
    content: typing.Union[str, typing.List[str]]
