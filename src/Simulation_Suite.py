from Simulation_Run import Run
from Evaluation import Evaluation
from Decomposition_Algorithms import gljd,exact,qbvn,double,qbvn_cover

heuristics = {
    "GLJD": gljd,
    "EXACT": exact,
    "QBVN": qbvn,
    "DOUBLE":double,
    "QBVN_Cover": qbvn_cover
}
seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
switch_sizes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25]
max_queue_lengths = [10,25,50]
simulation_lengths = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

header = "heuristic,switch_size,max_queue_length,simulation_length,packet_delay_average,packet_delay_variance,packet_delay_max,packet_delay_min,queue_length_average,queue_length_variance,queue_length_max,queue_length_min,permutation_matrix_amount_average,permutation_matrix_amount_variance,permutation_matrix_amount_max,permutation_matrix_amount_min,throughput_average,throughput_variance,throughput_max,throughput_min"

with open("data/results.csv", "w+") as file:
    file.write(header + "\n")
    for h in heuristics:
        for s in switch_sizes:
            for m in max_queue_lengths:
                for l in simulation_lengths:
                    evaluation = Evaluation()
                    for i in seeds:
                        print("##### Run {} #####".format(i + 1))
                        run = Run(heuristics[h], s, m, l, i, evaluation)
                        run.evaluate()
                    line = h + "," + str(s) + "," + str(m) + "," + str(l) + "," + evaluation.get_results_csv_line() + "\n"
                    file.write(line)
