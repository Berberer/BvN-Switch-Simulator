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

def query_data(columns_clause, where_clause):
    query = "SELECT {} FROM results WHERE {}".format(columns_clause, where_clause)
    return zip(*engine.execute(query).fetchall())

def plot_line_with_std_deviation(x, x_label, y, y_label, where_clause, file_name):
    pyplot.figure()
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    columns_clause = "{}, {}_average, {}_variance".format(x, y, y)
    for heuristic in ["GLJD"]:
        where_clause =  "heuristic='{}' AND {}".format(heuristic, where_clause)
        sizes, averages, variances = query_data(columns_clause, where_clause)
        pyplot.errorbar(sizes, averages, yerr=numpy.sqrt(variances), color=colors[heuristic], label=heuristic)
    pyplot.legend()
    pyplot.tight_layout()
    pyplot.savefig("vis/{}".format(file_name))

def plot_heuristic_throughput_for_different_queue_lengths(simulation_length, heuristic, max_queue_lengths, file_name):
    max_queue_lengths.sort(reverse=True)
    pyplot.figure()
    pyplot.xlabel("Switch Size")
    pyplot.ylabel("Throughput")
    columns_clause = "switch_size, throughput_average, throughput_variance"
    for i, max_queue_length in enumerate(max_queue_lengths):
        where_clause =  "heuristic='{}' AND simulation_length={} AND max_queue_length={}".format(heuristic, simulation_length, max_queue_length)
        sizes, averages, variances = query_data(columns_clause, where_clause)
        c = colors[heuristic]
        r = float(i) / float(len(max_queue_lengths))
        if c[0]==0:
            c = (r, c[1], c[2], c[3])
        if c[1]==0:
            c = (c[0], r, c[2], c[3])
        if c[2]==0:
            c = (c[0], c[1], r, c[3])
        pyplot.errorbar(sizes, averages, yerr=numpy.sqrt(variances), color=c, label="<= {}".format(str(max_queue_length)))
    pyplot.legend()
    pyplot.tight_layout()
    pyplot.savefig("vis/{}".format(file_name))

where_clause = "simulation_length=100 AND max_queue_length=50 AND load=1.0"
plot_line_with_std_deviation("switch_size", "Switch Size", "throughput", "Throughput", where_clause, "SwitchSizeToThroughput.png")
plot_line_with_std_deviation("switch_size", "Switch Size", "permutation_matrix_amount", where_clause, "Number of Permutation Matrices", "SwitchSizeToMatrixNumber.png")
plot_line_with_std_deviation("switch_size", "Switch Size", "queue_length", "Average Queue Length", where_clause, "SwitchSizeToQueueLength.png")
plot_line_with_std_deviation("switch_size", "Switch Size", "packet_delay", "Average Packet Delay", where_clause, "SwitchSizeToPacketDelay.png")

where_clause = "simulation_length=100 AND max_queue_length=50 and switch_size=10"
plot_line_with_std_deviation("load", "Load", "throughput", "Throughput", where_clause, "LoadToThroughput.png")
plot_line_with_std_deviation("load", "Load", "queue_length", "Average Queue Length", where_clause, "LoadToQueueLength.png")

plot_heuristic_throughput_for_different_queue_lengths(100, "GLJD", [10, 25, 50], "MaxQueueLengthsGLJD.png")
plot_heuristic_throughput_for_different_queue_lengths(100, "QBVN", [10, 25, 50], "MaxQueueLengthsQBVN.png")
plot_heuristic_throughput_for_different_queue_lengths(100, "QBVN_Cover", [10, 25, 50], "MaxQueueLengthsQBVN_Cover.png")
plot_heuristic_throughput_for_different_queue_lengths(100, "EXACT", [10, 25, 50], "MaxQueueLengthsEXACT.png")
plot_heuristic_throughput_for_different_queue_lengths(100, "DOUBLE", [10, 25, 50], "MaxQueueLengthsDOUBLE.png")
