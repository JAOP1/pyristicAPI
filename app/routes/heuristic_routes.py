"""Routes that perform the selected metaheuristic."""
import logging
import traceback
from fastapi import HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from pyristic.utils import get_stats
from app.services import evolutionary as ea_utils
from app.services import simulated_annealing as sa_utils
from app.utils.validations import ValidateFiles
from app.utils.generic import transform_values_dict, ModulesHandler
from app.models import EvolutionaryAlgorithm, OptimizerArguments, EvolutionaryOperators

LOGGER = logging.getLogger(__name__)

heuristics_router = APIRouter(
    prefix="/optimize",
    tags=["Heuristics"],
)


@heuristics_router.post(
    "/evolutionary/{optimizer}",
    status_code=200,
    dependencies=[Depends(ValidateFiles(["function", "constraints", "search_space"]))],
)
def execute_optimizer_request(
    optimizer: EvolutionaryAlgorithm,
    num_executions: int,
    arguments_optimizer: OptimizerArguments,
    config_operators: EvolutionaryOperators,
):
    """
    Perform an evolutionary algorithm.

    Arguments:
        - optimizer: the evolutionary algorithm selected.
        - num_executions: integer number that is the number of times executed the algorithm.
        - arguments_optimizer: dictionary with the key arguments for the optimize method.
        - config_operators: dictionary with the operators applied to the algorithm.
    """
    try:
        LOGGER.info("Creating configuration for %s", optimizer)
        configuration = ea_utils.create_evolutionary_config(
            optimizer, config_operators.methods
        )
        LOGGER.info("\n%s", configuration)
        evolutionary_algorithm = ea_utils.create_evolutionary_algorithm(
            optimizer, configuration
        )
        LOGGER.info("Execute %s - %s", optimizer, num_executions)
        statistics_algorithm = transform_values_dict(
            get_stats(
                evolutionary_algorithm,
                num_executions,
                [],
                arguments_optimizer.arguments,
                verbose=True,
            )
        )
        LOGGER.info("End with success.")
    except Exception as exc:
        error_detail = traceback.format_exc()
        LOGGER.error(error_detail)
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return JSONResponse(content=statistics_algorithm)


@heuristics_router.post(
    "/SimulatedAnnealing",
    status_code=200,
    dependencies=[
        Depends(
            ValidateFiles(
                [
                    "function",
                    "constraints",
                    "SA_neighbor_generator",
                    "generator_initial_solution",
                ]
            )
        )
    ],
)
def execute_sa_request(num_executions: int, arguments_optimizer: OptimizerArguments):
    """
    Perform Simulated Annealing algorithm.

    Arguments:
        - num_executions: integer number that is the number of times executed the algorithm.
        - arguments_optimizer: dictionary with the key arguments for the optimize method.
    """
    try:
        LOGGER.info("Starting SA optimization execution")
        get_initial_solution = ModulesHandler().get_method_by_module(
            "generator_initial_solution", "generate_initial_solution"
        )
        sa_algorithm = sa_utils.create_simulatedannealing_algorithm()
        LOGGER.info("created SA algorithm")
        statistics_algorithm = transform_values_dict(
            get_stats(
                sa_algorithm,
                num_executions,
                [get_initial_solution],
                arguments_optimizer.arguments,
                verbose=True,
            )
        )
        LOGGER.info("End with success.")
    except Exception as exc:
        error_detail = traceback.format_exc()
        LOGGER.error(error_detail)
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return JSONResponse(content=statistics_algorithm)
