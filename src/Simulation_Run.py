import random
import simpy
import numpy as np
from Evaluation import Evaluation
from simulated.Traffic_Generator import Traffic_Generator
from simulated.Switch import Switch
from simulated.Schedule import Schedule

class Run(object):

    def __init__(self, heuristic, size, seed, evaluation):
        super(Run, self).__init__()
        random.seed(seed)
        self._heuristic = heuristic
        self._traffic_generator = Traffic_Generator(size, seed)
        traffic_matrix = self._traffic_generator.get_traffic_matric()
        print(traffic_matrix)
        permutation_matrices, probabilities = self._heuristic(traffic_matrix)
        schedule = Schedule(permutation_matrices,probabilities)
        self._switch = Switch(size, size, schedule)
        self._env = simpy.Environment()
        self._evaluation = evaluation
        self._evaluation.add_number_of_permutation_matrices(len(permutation_matrices))
        self._generated_packets = 0
        self._forwarded_packets = 0

    def evaluate(self):
        self._env.process(self.traffic_generation_step(self._env, 1))
        self._env.process(self.switch_forwarding_step(self._env, 1))
        self._env.run(until=10)
        self._evaluation.add_throughput(self._forwarded_packets / self._generated_packets)

    def traffic_generation_step(self, env, tick):
        while True:
            generated_packets = self._traffic_generator.generate_packets(env.now)
            self._switch.packets_arrive(generated_packets)
            self._generated_packets = self._generated_packets + len(generated_packets)
            print("Generated traffic in step {}: {}".format(
                env.now, ', '.join(str(x) for x in generated_packets)
                )
            )
            yield env.timeout(tick)

    def switch_forwarding_step(self, env, tick):
        while True:
            forwarded_packets = self._switch.forward_packets()
            self._forwarded_packets = self._forwarded_packets + len(forwarded_packets)
            self._evaluation.add_forwarded_packets(forwarded_packets, env.now)
            self._evaluation.add_queue_lengths(self._switch.get_queue_lengths())
            yield env.timeout(tick)