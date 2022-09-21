"""
Method required to implement simulated annealing algorithm of pyristic. 
"""
from fastapi import HTTPException
from pyristic.heuristic import SimulatedAnnealing
import utils

def create_simulatedannealing_algorithm() -> SimulatedAnnealing:
    """
    Description:
        It creates a search algorithm based on simulated annealing algorithm.
    Arguments:
        - optimizer_arguments: dictionary with the keys required to perform the search.
    """
    try:
        function = utils.ModulesHandler().get_method_by_module('function','function')
        constraints = utils.ModulesHandler().get_method_by_module('constraints','ARRAY_CONSTRAINTS')
        generator = utils.ModulesHandler().get_method_by_module('SA_neighbor_generator','neighbor_generator')
        return SimulatedAnnealing(function, constraints, generator)
    except Exception as error:
        raise HTTPException(
            status_code= 404,
            detail= str(error)
        )
