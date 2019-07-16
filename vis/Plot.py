import numpy
import pandas
from matplotlib import pyplot

simulation_results = pandas.read_csv("data/results.csv", sep=",", header=0)

heuristics = [ "GLJD", "QBVN", "QBVN_Cover", "EXACT", "DOUBLE" ]
colors = {
    "GLJD": (0, 1, 0, 0.5),
    "QBVN": (0, 0, 1, 0.5),
    "QBVN_Cover": (0, 1, 1, 0.5),
    "EXACT": (1, 0, 0, 0.5),
    "DOUBLE": (1, 0, 1, 0.5)
}

heuristic_data = {}
for h in heuristics:
    heuristic_data[h] = simulation_results[simulation_results["heuristic"] == h]

def plot_switch_size_to_result(simulation_length, result_row, result_label, file_name):
    switch_sizes = heuristic_data[heuristics[0]]["switch_size"].unique()
    pyplot.figure()
    pyplot.xlabel("Switch Size")
    pyplot.ylabel(result_label)
    for heuristic, data in heuristic_data.items():
        data_with_correct_length = data[data["simulation_length"] == simulation_length]
        values = data_with_correct_length["{}_average".format(result_row)].to_numpy()
        std_deviations = numpy.sqrt(data_with_correct_length["{}_variance".format(result_row)].to_numpy())
        pyplot.errorbar(switch_sizes, values, yerr=std_deviations, color=colors[heuristic], label=heuristic)
    pyplot.legend()
    pyplot.tight_layout()
    pyplot.savefig("vis/{}".format(file_name))

plot_switch_size_to_result(100, "throughput", "Throughput", "SwitchSizeToThroughput.png")
plot_switch_size_to_result(100, "permutation_matrix_amount", "Number of Permutation Matrices", "SwitchSizeToMatrixNumber.png")
plot_switch_size_to_result(100, "queue_length", "Average Queue Length", "SwitchSizeToQueueLength.png")
