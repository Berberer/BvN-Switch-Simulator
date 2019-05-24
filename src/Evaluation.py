import numpy as np

class Evaluation(object):

    def __init__(self, permutation_matrix_amount):
        super(Evaluation, self).__init__()
        self._delays = []
        self._queue_lengths = []
        self._permutation_matrix_amount = permutation_matrix_amount
        self._packets_generated = 0.0
        self._packets_forwarded = 0.0

    def add_forwarded_packets(self, packets, timestep):
        self._packets_forwarded = self._packets_forwarded + len(packets)
        for p in packets:
            self._delays.append(timestep - p.get_arrival_timestep())

    def add_queue_lengths(self, queue_lengths):
        self._queue_lengths = self._queue_lengths + queue_lengths

    def add_number_of_generated_packets(self, number_of_generated_packets):
        self._packets_generated = self._packets_generated + number_of_generated_packets

    def get_results(self):
        delays = np.array(self._delays)
        queue_lengths = np.array(self._queue_lengths)
        return {
            "average_packet_delay": np.mean(delays),
            "max_packet_delay": delays.max(),
            "average_queue_length": np.mean(queue_lengths),
            "max_queue_length": queue_lengths.max(),
            "permutation_matrix_amount": self._permutation_matrix_amount,
            "throughput": self._packets_forwarded / self._packets_generated
        }
