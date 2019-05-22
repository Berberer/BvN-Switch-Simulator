import random

class Schedule(object):

    def __init__(self, permutation_matrices, probabilities):
        super(Schedule, self).__init__()
        self._permutation_matrices = permutation_matrices
        self._probabilities = probabilities

    def get_random_permutation_matrix(self):
        index = 0
        sum = 0
        chance = random.uniform(0, 1)
        for index, probability in enumerate(self._probabilities):
            sum = sum + probability
            if chance <= sum:
                return self._permutation_matrices[index]
