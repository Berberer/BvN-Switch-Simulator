import random
from Packet import Packet

class Traffic_Generator(object):

    def __init__(self, traffic_matrix):
        super(Traffic_Generator, self).__init__()
        self._traffic_matrix = traffic_matrix

    def generate_packets(self, timestep):
        packets = []
        for input, probabilities in enumerate(self._traffic_matrix):
            chance = random.uniform(0, 1)
            output = -1
            sum = 0

            for o, probability in enumerate(probabilities):
                sum = sum + probability
                if chance <= sum:
                    output = o
                    break

            if output != -1:
                packets.append(Packet(input, output, timestep))

        return packets
