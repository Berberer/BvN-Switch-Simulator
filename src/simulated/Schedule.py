import random
import numpy as np

class Schedule(object):

    def __init__(self, permutation_matrices, probabilities):
        super(Schedule, self).__init__()
        self._permutation_matrices = permutation_matrices
        max_probability = sum(probabilities)
        # scale probabilities to a distribution
        self._probabilities = [i * (1/max_probability) for i in probabilities]

    def get_random_permutation_matrix(self):
        indices = np.arange(len(self._permutation_matrices))
        choice = np.random.choice(indices, p=self._probabilities)
        return self._permutation_matrices[choice]
