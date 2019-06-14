import json
import click
from Decomposition_Algorithms import gljd,exact,qbvn
from Simulation_Run import Run
from Evaluation import Evaluation

# TODO: Add the remaining heuristics
heuristics = {
    "GLJD": gljd,
    "EXACT": exact,
    "QBVN": qbvn
}

@click.command()
@click.option(
    "--heuristic",
    type=click.Choice(heuristics.keys()),
    prompt="Desired heuristic",
    help="Choose the decomposition heuristic to evaluate."
)
@click.option(
    "--size",
    type=click.IntRange(min=2),
    prompt="Size of the switch, i.e. number of input ports and output ports",
    help="Select how many input ports and output ports the simulated switch should have (at least 2)"
)
@click.option(
    "--runs",
    type=click.IntRange(min=1),
    prompt="Number of runs",
    help="Select how many simulation runs shall be perfomed (at least 1)"
)
@click.option(
    "--length",
    type=click.IntRange(min=1),
    prompt="Length of the runs",
    help="Select how many timesteps one runs shall be simulated (at least 1)"
)
def simulate(heuristic, size, runs, length):
    evaluation = Evaluation()
    for i in range(runs):
        print("##### Run {} #####".format(i + 1))
        run = Run(heuristics[heuristic], size, length, i, evaluation)
        run.evaluate()
    print("\n\n##### Results #####")
    print(json.dumps(evaluation.get_results(), indent=4))
    file_name = "data/results_{}_steps_{}_size_{}_runs_{}.json".format(heuristic, length, size, runs)
    with open(file_name, "w+") as file:
        json.dump(evaluation.get_results(), file, indent=4)

if __name__ == "__main__":
    simulate()
