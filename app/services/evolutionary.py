"""Methods required to implement a evolutionary algorithm of pyristic."""
import typing
from pyristic.heuristic import Genetic, EvolutionStrategy, EvolutionaryProgramming
from pyristic.utils.evolutionary_config import OptimizerConfig
import pyristic.utils.operators as pc_method
import pyristic.utils.helpers as pc_utils
from app.models import EvolutionaryAlgorithm, EvolutionaryOperators
from app.utils.generic import ModulesHandler


def get_evolutionary_method(algorithm, operator_type, config):
    """
    Provide the official method or custom method that envolve any step.

    Arguments:
        - algorithm: It helps us to know the algorithm GA,EE or EP.
        - operator_type: It says the method to configure.
        - config: Object that has all configuration and provide us the method name.
    """
    method_name = config[operator_type].operator_name
    if method_name != "CustomMethod":
        search_location = pc_method
        if operator_type == "setter_invalid_solution":
            search_location = pc_utils
        return getattr(search_location, method_name)
    return ModulesHandler().get_method_by_module(
        f"{algorithm}_{operator_type}", "CustomMethod"
    )


def create_evolutionary_config(
    algorithm_type: EvolutionaryAlgorithm, config: EvolutionaryOperators
) -> OptimizerConfig:
    """
    Create the evolutionary configuration for the specific algorithm.

    Arguments:
        - algorithm_type: Recives a string that correspond to one of the three
            types of algorithms (GA,EE,EP).
        - config: dictionary with the operators desired
    """
    optional_methods = ["init_population"]
    methods_to_set = [
        "mutation_operator",
        "survivor_selector",
        "setter_invalid_solution",
        "init_population",
    ]

    if algorithm_type == "GA":
        methods_to_set += ["crossover_operator", "parent_selector"]
    elif algorithm_type == "EE":
        methods_to_set += [
            "adaptive_crossover_operator",
            "adaptive_mutation_operator",
            "crossover_operator",
        ]
    else:
        methods_to_set += ["adaptive_mutation_operator"]
    pyristic_config = OptimizerConfig()
    for operator_type in methods_to_set:
        if not config.get(operator_type, False) and operator_type in optional_methods:
            continue

        method = get_evolutionary_method(algorithm_type, operator_type, config)
        try:
            pyristic_config.methods[operator_type] = method(
                *config[operator_type].parameters
            )
        except TypeError:
            # WORKAROUND
            pyristic_config.methods[operator_type] = method(
                *[config[operator_type].parameters]
            )

    return pyristic_config


def create_evolutionary_algorithm(
    algorithm_type: EvolutionaryAlgorithm, evolutionary_config: OptimizerConfig
) -> typing.Union[Genetic, EvolutionStrategy, EvolutionaryProgramming]:
    """
    Create an instance of evolutionary algorithm selected with the configuration.

    Arguments:
        - algorithm_type: string that represent the tipe of algorithm.
        - evolutionary_config: Optimization configuration that provides the methods
            needed for the algorithm.
    """
    initialize_arguments = {
        "function": ModulesHandler().get_method_by_module(
            "function", "aptitude_function"
        ),
        "decision_variables": ModulesHandler().get_method_by_module(
            "search_space", "DECISION_VARIABLES"
        ),
        "constraints": ModulesHandler().get_method_by_module(
            "constraints", "ARRAY_CONSTRAINTS"
        ),
        "bounds": ModulesHandler().get_method_by_module("search_space", "BOUNDS"),
        "config": evolutionary_config,
    }
    if algorithm_type == "GA":
        return Genetic(**initialize_arguments)
    if algorithm_type == "EE":
        return EvolutionStrategy(**initialize_arguments)
    return EvolutionaryProgramming(**initialize_arguments)
