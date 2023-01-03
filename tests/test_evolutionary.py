import unittest
from unittest.mock import patch
from collections import namedtuple
import search_utils.evolutionary as ev_utils
class TestEvolutionary(unittest.TestCase):
    """
    Test suite for evolutionary file.
    """
    method = namedtuple('method', ['operator_name', 'parameters'])

    def test_get_evolutionary_method(self):
        config = {
            'mutation_operator': self.method('BinaryMutator',''),
            'setter_invalid_solution': self.method('ContinuosFixer','')
        }
        #It should return the pyristic method
        #when the method name isn't CustomMethod nor setter_invalid_solution.
        method = ev_utils.get_evolutionary_method('GA', 'mutation_operator', config)()
        self.assertEqual(type(method).__name__, 'BinaryMutator')

        #It should return the setter method
        #when the operator type is setter_invalid_solution.
        method = ev_utils.get_evolutionary_method('GA', 'setter_invalid_solution', config)([-1,1])
        self.assertEqual(type(method).__name__, 'ContinuosFixer')

    def test_create_evolutionary_config(self):
        #It should return a GA configuration.
        config = {
            'crossover_operator': self.method('IntermediateCrossover',[0.5]),
            'mutation_operator': self.method('UniformMutator',[-3,3]),
            'survivor_selector': self.method('MergeSelector',[]),
            'setter_invalid_solution': self.method('ContinuosFixer',[]),
            'init_population': self.method('RandomUniformPopulation',[2, [-3,3]]),
            'parent_selector': self.method('TournamentSampler',[3,0.5])
        }
        genetic_config = ev_utils.create_evolutionary_config('GA', config)
        self.assertEqual(type(genetic_config).__name__, 'OptimizerConfig')
        for key, value in config.items():
            self.assertEqual(
                value.operator_name,
                type(genetic_config.methods[key]).__name__
            )

        #It should raise an exception when the method isn't found.
        config['crossover_operator'] = self.method('NotMethod',[])
        with self.assertRaises(Exception):
            ev_utils.create_evolutionary_config('GA',config)


if __name__ == '__main__':
    unittest.main(verbosity=3)