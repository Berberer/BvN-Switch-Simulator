import click
from Decomposition_Algorithms import gljd
from Simulation_Run import Run

# TODO: Add the remaining heuristics
heuristics = {
    "GLJD": gljd
}

@click.command()
@click.option(
    "--heuristic",
    type=click.Choice(heuristics.keys()),
    prompt="Desired heuristic",
    help="Choose the decomposition heuristic to evaluate."
)
@click.option(
    "--runs",
    type=click.IntRange(min=1),
    prompt="Number of runs",
    help="Select how many simulation runs shall be perfomed, but at least 1."
)
def simulate(heuristic, runs):
    for i in range(runs):
        print("##### Run {} #####".format(i + 1))
        run = Run(heuristics[heuristic], i)
        print(str(run.evaluate()))

if __name__ == "__main__":
    simulate()
