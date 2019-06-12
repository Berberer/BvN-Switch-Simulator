import numpy as np

class Evaluation(object):

    def __init__(self):
        super(Evaluation, self).__init__()
        self._delays = []
        self._queue_lengths = []
        self._permutation_matrix_amounts = []
        self._throughputs = []

    def add_forwarded_packets(self, packets, timestep):
        for p in packets:
            self._delays.append(timestep - p.get_arrival_timestep())

    def add_queue_lengths(self, queue_lengths):
        self._queue_lengths = self._queue_lengths + queue_lengths

    def add_throughput(self, throughput):
        self._throughputs.append(throughput)

    def add_number_of_permutation_matrices(self, number_of_permutation_matrices):
        self._permutation_matrix_amounts.append(number_of_permutation_matrices)

    def get_results(self):
        delays = np.array(self._delays)
        queue_lengths = np.array(self._queue_lengths)
        permutation_matrix_amount =  np.array(self._permutation_matrix_amounts)
        throughputs = np.array(self._throughputs)
        return {
            "packet_delay_average": float(np.mean(delays)),
            "packet_delay_variance": float(np.var(delays)),
            "packet_delay_max": float(delays.max()),
            "packet_delay_min": float(delays.min()),
            "queue_length_average": float(np.mean(queue_lengths)),
            "queue_length_variance": float(np.var(queue_lengths)),
            "queue_length_max": float(queue_lengths.max()),
            "queue_length_min": float(queue_lengths.min()),
            "permutation_matrix_amount_average": float(np.mean(permutation_matrix_amount)),
            "permutation_matrix_amount_variance": float(np.var(permutation_matrix_amount)),
            "permutation_matrix_amount_max": float(permutation_matrix_amount.max()),
            "permutation_matrix_amount_min": float(permutation_matrix_amount.min()),
            "throughput_average": float(np.mean(throughputs)),
            "throughput_variance": float(np.var(throughputs)),
            "throughput_max": float(throughputs.max()),
            "throughput_min": float(throughputs.min())
        }

    def get_results_csv_line(self):
        results = self.get_results()
        return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            str(results["packet_delay_average"]),
            str(results["packet_delay_variance"]),
            str(results["packet_delay_max"]),
            str(results["packet_delay_min"]),
            str(results["queue_length_average"]),
            str(results["queue_length_variance"]),
            str(results["queue_length_max"]),
            str(results["queue_length_min"]),
            str(results["permutation_matrix_amount_average"]),
            str(results["permutation_matrix_amount_variance"]),
            str(results["permutation_matrix_amount_max"]),
            str(results["permutation_matrix_amount_min"]),
            str(results["throughput_average"]),
            str(results["throughput_variance"]),
            str(results["throughput_max"]),
            str(results["throughput_min"]),
        )
