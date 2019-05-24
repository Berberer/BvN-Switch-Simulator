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
    "--size",
    type=click.IntRange(min=2),
    prompt="Size of the switch, i.e. number of input ports and output ports",
    help="Select how many input ports and output ports the simulated switch should have."
)
@click.option(
    "--runs",
    type=click.IntRange(min=1),
    prompt="Number of runs",
    help="Select how many simulation runs shall be perfomed, but at least 1."
)
def simulate(heuristic, size, runs):
    for i in range(runs):
        print("##### Run {} #####".format(i + 1))
        run = Run(heuristics[heuristic], size, i)
        print(str(run.evaluate()))

if __name__ == "__main__":
    simulate()
