import random
import numpy as np
from sinkhorn_knopp import sinkhorn_knopp
from simulated.Packet import Packet

class Traffic_Generator(object):

    def __init__(self, size, seed, load):
        super(Traffic_Generator, self).__init__()
        self._size = size
        self._seed = seed
        self._load = load

    def generate_doubly_stochastic_traffic(self):
        np.random.seed(self._seed)
        sk = sinkhorn_knopp.SinkhornKnopp()
        self._traffic_matrix = sk.fit(np.random.rand(self._size, self._size))
        self._traffic_matrix = self._traffic_matrix * self._load
        return self._traffic_matrix

    def generate_packets(self, timestep):
        packets = []
        for input in range(0, self._size):
            output_probas = self._traffic_matrix[input]
            # check if we can use the probabilities
            if all(i == 0 for i in output_probas):
                output = -1
            else:
                # flip a coin according to load if we want to generate a packet
                generate_packet = np.random.choice([True, False], p = [self._load, 1-self._load])
                if generate_packet:
                    proba_sum = sum(output_probas)
                    scaled_probas = [i * (1/proba_sum) for i in output_probas]
                    output_indices = np.arange(self._size)
                    output = np.random.choice(output_indices, p=scaled_probas)
                else:
                    output=-1
            if output != -1:
                packets.append(Packet(input, output, timestep))
        return packets
