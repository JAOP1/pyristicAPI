"""
Methods required to implement a evolutionary algorithm of pyristic.
"""
import typing
from fastapi import HTTPException
from pyristic.heuristic import Genetic, EvolutionStrategy, EvolutionaryProgramming
from pyristic.utils.evolutionary_config import OptimizerConfig
import pyristic.utils.operators as pc_method
import pyristic.utils.helpers as pc_utils
import argument_types as arg_api
import utils


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
                search_location = pc_utils
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
        initialize_arguments = {
            'function':utils.get_method_by_local_file('function','aptitude_function'),
            'decision_variables': utils.get_method_by_local_file(
                                            'search_space',
                                            'DECISION_VARIABLES'
                                ),
            'constraints':utils.get_method_by_local_file('constraints','ARRAY_CONSTRAINTS'),
            'bounds':utils.get_method_by_local_file('search_space','BOUNDS'),
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
