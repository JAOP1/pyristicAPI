import unittest
from unittest.mock import patch
from collections import namedtuple
from fastapi import HTTPException
import search_utils.evolutionary as ev_utils


class TestEvolutionary(unittest.TestCase):
    """
    Test suite for evolutionary file.
    """

    method = namedtuple("method", ["operator_name", "parameters"])

    @patch("utils.ModulesHandler")
    def test_get_evolutionary_method(self, mock_module_handler):
        """
        Tests for the get_evolutionary_method function.
        """
        config = {
            "mutation_operator": self.method("BinaryMutator", []),
            "setter_invalid_solution": self.method("ContinuosFixer", []),
            "crossover_operator": self.method("CustomMethod", []),
        }
        # It should return the pyristic method
        # when the method name isn't CustomMethod nor setter_invalid_solution.
        method = ev_utils.get_evolutionary_method("GA", "mutation_operator", config)()
        self.assertEqual(type(method).__name__, "BinaryMutator")

        # It should return the setter method
        # when the operator type is setter_invalid_solution.
        method = ev_utils.get_evolutionary_method(
            "GA", "setter_invalid_solution", config
        )([-1, 1])
        self.assertEqual(type(method).__name__, "ContinuosFixer")

        # It should return custom method when the method_name is CustomMethod.
        method = ev_utils.get_evolutionary_method("GA", "crossover_operator", config)()
        self.assertEqual(mock_module_handler.call_count, 1)

        # It should return an exception when the operator isn't found.
        config["mutation_operator"] = self.method("FakeMethod", "")
        with self.assertRaises(AttributeError):
            ev_utils.get_evolutionary_method("GA", "mutation_operator", config)

    def test_create_evolutionary_config(self):
        """
        Tests for the create_evolutionary_config function.
        """

        def match_validation(result_config, expected_config):
            self.assertEqual(type(result_config).__name__, "OptimizerConfig")
            for key, value in expected_config.items():
                self.assertEqual(
                    value.operator_name, type(result_config.methods[key]).__name__
                )

        # It should return a GA config with all methods.
        config = {
            "crossover_operator": self.method("IntermediateCrossover", [0.5]),
            "mutation_operator": self.method("UniformMutator", [-3, 3]),
            "survivor_selector": self.method("MergeSelector", []),
            "setter_invalid_solution": self.method("ContinuosFixer", []),
            "init_population": self.method("RandomUniformPopulation", [2, [-3, 3]]),
            "parent_selector": self.method("TournamentSampler", [3, 0.5]),
        }
        genetic_config = ev_utils.create_evolutionary_config("GA", config)
        match_validation(genetic_config, config)
        # It should return a GA config without optional methods.
        del config["init_population"]
        genetic_config = ev_utils.create_evolutionary_config("GA", config)
        match_validation(genetic_config, config)

        # It should raise an exception when the method isn't found.
        config["crossover_operator"] = self.method("NotMethod", [])
        with self.assertRaises(Exception):
            ev_utils.create_evolutionary_config("GA", config)

        # It should return a EE config.
        config = {
            "mutation_operator": self.method("SigmaMutator", []),
            "crossover_operator": self.method("DiscreteCrossover", []),
            "survivor_selector": self.method("MergeSelector", []),
            "setter_invalid_solution": self.method("ContinuosFixer", [-1, 1]),
            "adaptive_crossover_operator": self.method("IntermediateCrossover", []),
            "adaptive_mutation_operator": self.method("MultSigmaAdaptiveMutator", 2),
        }
        evolutionary_strategy_config = ev_utils.create_evolutionary_config("EE", config)
        match_validation(evolutionary_strategy_config, config)

        # It should return a EP config.
        config = {
            "mutation_operator": self.method("SigmaMutator", []),
            "survivor_selector": self.method("MergeSelector", []),
            "setter_invalid_solution": self.method("ContinuosFixer", [-1, 1]),
            "adaptive_mutation_operator": self.method(
                "SigmaEpAdaptiveMutator", [3, 0.5]
            ),
        }
        evolutive_programming_config = ev_utils.create_evolutionary_config("EP", config)
        match_validation(evolutive_programming_config, config)

    @patch("utils.ModulesHandler")
    def test_create_evolutionary_algorithm(self, mock_modules_hanler):
        """
        Tests for the create_evolutionary_algorithm function.
        """
        # It should return a GA algorithm class when it created successfully.
        config = {
            "crossover_operator": self.method("IntermediateCrossover", [0.5]),
            "mutation_operator": self.method("UniformMutator", [-3, 3]),
            "survivor_selector": self.method("MergeSelector", []),
            "setter_invalid_solution": self.method("ContinuosFixer", []),
            "init_population": self.method("RandomUniformPopulation", [2, [-3, 3]]),
            "parent_selector": self.method("TournamentSampler", [3, 0.5]),
        }
        genetic_config = ev_utils.create_evolutionary_config("GA", config)
        algorithm = ev_utils.create_evolutionary_algorithm("GA", genetic_config)
        self.assertEqual(type(algorithm).__name__, "Genetic")

        # It should return a EE algorithm class when it created successfully.
        config = {
            "mutation_operator": self.method("SigmaMutator", []),
            "crossover_operator": self.method("DiscreteCrossover", []),
            "survivor_selector": self.method("MergeSelector", []),
            "setter_invalid_solution": self.method("ContinuosFixer", [-1, 1]),
            "adaptive_crossover_operator": self.method("IntermediateCrossover", []),
            "adaptive_mutation_operator": self.method("MultSigmaAdaptiveMutator", 2),
        }
        evolutionary_strategy_config = ev_utils.create_evolutionary_config("EE", config)
        algorithm = ev_utils.create_evolutionary_algorithm(
            "EE", evolutionary_strategy_config
        )
        self.assertEqual(type(algorithm).__name__, "EvolutionStrategy")

        # It should return a EP algorithm class when it created successfully.
        config = {
            "mutation_operator": self.method("SigmaMutator", []),
            "survivor_selector": self.method("MergeSelector", []),
            "setter_invalid_solution": self.method("ContinuosFixer", [-1, 1]),
            "adaptive_mutation_operator": self.method(
                "SigmaEpAdaptiveMutator", [3, 0.5]
            ),
        }
        evolutive_programming_config = ev_utils.create_evolutionary_config("EP", config)
        algorithm = ev_utils.create_evolutionary_algorithm(
            "EP", evolutive_programming_config
        )
        self.assertEqual(type(algorithm).__name__, "EvolutionaryProgramming")

        # It should return an exception when it couldn't create the algorithm.
        mock_modules_hanler.side_effect = Exception("Couldn't get the method.")
        with self.assertRaises(Exception):
            ev_utils.create_evolutionary_algorithm("EP", evolutive_programming_config)


if __name__ == "__main__":
    unittest.main(verbosity=3)
