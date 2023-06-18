"""Method required to implement simulated annealing algorithm of pyristic."""
from fastapi import HTTPException
from pyristic.heuristic import SimulatedAnnealing
from app.utils.generic import ModulesHandler


def create_simulatedannealing_algorithm() -> SimulatedAnnealing:
    """
    Create a search algorithm based on simulated annealing algorithm.

    Arguments:
        - optimizer_arguments: dictionary with the keys required to perform the search.
    """
    try:
        function = ModulesHandler().get_method_by_module("function", "function")
        constraints = ModulesHandler().get_method_by_module(
            "constraints", "ARRAY_CONSTRAINTS"
        )
        generator = ModulesHandler().get_method_by_module(
            "SA_neighbor_generator", "neighbor_generator"
        )
        return SimulatedAnnealing(function, constraints, generator)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
