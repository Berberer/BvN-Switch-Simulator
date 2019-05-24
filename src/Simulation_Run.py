import simpy
import numpy as np
import random
from simulated.Traffic_Generator import Traffic_Generator
from simulated.Switch import Switch
from simulated.Schedule import Schedule

class Run(object):

    def __init__(self, heuristic, seed):
        super(Run, self).__init__()
        self._heuristic = heuristic
        random.seed(seed)
        # TODO: Replace hard-coded matrix with a automatically created one
        traffic_matrix = np.array([
            [0.38, 0, 0.22, 0.4],
            [0.11, 0.24, 0.6, 0.05],
            [0, 0.53, 0.14, 0.33],
            [0.51, 0.23, 0.04, 0.22]
        ])
        self._traffic_generator = Traffic_Generator(traffic_matrix)
        permutation_matrices, probabilities = self._heuristic(traffic_matrix)
        schedule = Schedule(permutation_matrices,probabilities)
        self._switch = Switch(traffic_matrix.shape[0], traffic_matrix.shape[1], schedule)
        self._env = simpy.Environment()

    def evaluate(self):
        self._env.process(self.traffic_generation_step(self._env, 1))
        self._env.process(self.switch_forwarding_step(self._env, 1))
        self._env.run(until=10)
        # TODO: Create actual evaluations
        return {
            "run_complete": True
        }

    def traffic_generation_step(self, env, tick):
        while True:
            generated_packets = self._traffic_generator.generate_packets(tick)
            self._switch.packets_arrive(generated_packets)
            print("Generated traffic in step {}: {}".format(
                tick, ', '.join(str(x) for x in generated_packets)
                )
            )
            yield env.timeout(tick)

    def switch_forwarding_step(self, env, tick):
        while True:
            print("Forwarding:")
            self._switch.forward_packets()
            yield env.timeout(tick)
