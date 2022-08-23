import typing
import os
import numpy as np
from fastapi import HTTPException
from pyristic.heuristic import Genetic, EvolutionStrategy, EvolutionaryProgramming
from pyristic.utils.evolutionary_config import OptimizerConfig
import pyristic.utils.operators as pc_method
import pyristic.utils.helpers as utils
import argument_types as arg_api
import settings


def create_evolutionary_config(
    algorithm_type: arg_api.EvolutionaryAlgorithm,
    config: arg_api.EvolutionaryOperators) -> OptimizerConfig:
    """
    Description:
        It creates the evolutionary configuration for the specific algorithm.
        If there is missing one required key returns to you an error message.
    Arguments:
        - algorithm_type: Recives a string that correspond to one of the three
            types of algorithms (GA,EE,EP).
        - config: dictionary with the operators desired
    """
    required_keys = [
        'mutation_operator',
        'survivor_selector',
        'setter_invalid_solution'
        ]

    if algorithm_type == 'GA':
        required_keys += [
            'crossover_operator',
            'parent_selector'
        ]
    elif algorithm_type == 'EE':
        required_keys += [
            'adaptive_crossover_operator',
            'adaptive_mutation_operator',
            'crossover_operator'
        ]
    else:
        required_keys += [
            'adaptive_mutation_operator'
        ]

    pyristic_config = OptimizerConfig()
    for operator_type in required_keys:
        try:
            search_location = pc_method
            if operator_type == 'setter_invalid_solution':
                search_location = utils
            method = getattr(search_location, config[operator_type].operator_name)
            pyristic_config.methods[operator_type] = method(*config[operator_type].parameters)

        except Exception as error:
            raise HTTPException(
                status_code= 400,
                detail= f"Error in the key: '{operator_type}'.\n Error description:\n{str(error)}"
            )
    return pyristic_config

def create_evolutionary_algorithm(
    algorithm_type: arg_api.EvolutionaryAlgorithm,
    evolutionary_config: OptimizerConfig) -> typing.Union[
                                                        Genetic,
                                                        EvolutionStrategy,
                                                        EvolutionaryProgramming]:
    """
    Description:
        Returns a initialized evolutionary algorithm.
    Arguments:
        - algorithm_type: string that represent the tipe of algorithm.
        - evolutionary_config: Optimization configuration that provides the methods
            needed for the algorithm.
    """
    try:
        from optimization_problem.function import aptitude_function
        from optimization_problem.constraints import ARRAY_CONSTRAINTS
        from optimization_problem.search_space import BOUNDS, DECISION_VARIABLES
        initialize_arguments = {
            'function':aptitude_function,
            'decision_variables': DECISION_VARIABLES,
            'constraints':ARRAY_CONSTRAINTS,
            'bounds':BOUNDS,
            'config':evolutionary_config
        }
        if algorithm_type == 'GA':
            return Genetic(**initialize_arguments)
        elif algorithm_type == 'EE':
            return EvolutionStrategy(**initialize_arguments)
        else:
            return EvolutionaryProgramming(**initialize_arguments)

    except Exception as error:
        raise HTTPException(    
            status_code= 404,
            detail= str(error)
        )

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
    return data_obj
