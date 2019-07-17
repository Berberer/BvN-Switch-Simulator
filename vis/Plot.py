import numpy
import pandas
from matplotlib import pyplot
from sqlalchemy import create_engine

simulation_results = pandas.read_csv("data/results.csv", sep=",", header=0)
engine = create_engine('sqlite:///:memory:', echo=False)
simulation_results.to_sql('results', con=engine)

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

def query_data(columns_clause, where_clause):
    query = "SELECT {} FROM results WHERE {}".format(columns_clause, where_clause)
    return zip(*engine.execute(query).fetchall())

def plot_line_with_std_deviation(simulation_length, x, x_label, y, y_label, file_name):
    pyplot.figure()
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    for heuristic, data in heuristic_data.items():
        columns_clause = "{}, {}_average, {}_variance".format(x, y, y)
        where_clause =  "heuristic='{}' AND simulation_length={}".format(heuristic, simulation_length)
        sizes, averages, variances = query_data(columns_clause, where_clause)
        pyplot.errorbar(sizes, averages, yerr=numpy.sqrt(variances), color=colors[heuristic], label=heuristic)
    pyplot.legend()
    pyplot.tight_layout()
    pyplot.savefig("vis/{}".format(file_name))

plot_line_with_std_deviation(100, "switch_size", "Switch Size", "throughput", "Throughput", "SwitchSizeToThroughput.png")
plot_line_with_std_deviation(100, "switch_size", "Switch Size", "permutation_matrix_amount", "Number of Permutation Matrices", "SwitchSizeToMatrixNumber.png")
plot_line_with_std_deviation(100, "switch_size", "Switch Size", "queue_length", "Average Queue Length", "SwitchSizeToQueueLength.png")
plot_line_with_std_deviation(100, "switch_size", "Switch Size", "packet_delay", "Average Packet Delay", "SwitchSizeToPacketDelay.png")
