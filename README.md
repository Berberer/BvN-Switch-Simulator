# BvN-Switch-Simulator

Simluator for Birkhoff–von Neumann scheduling in a switch. Different heuristics for the scheduling are compared regarding metrics like packet delay, queue size, throughput, etc.

## Getting Started
### Install dependencies:
```bash
pip install -r requirements.txt
```
### Run a single simulation
To run a single simulation with the desired configuration and write the evaluation results into a JSON file there are the following possibilities:
* Run the simulator and select your simulation configuration interactively:
```bash
python src/Simulator.py
```
* Specify your configuration manually. For example in the case of GLJD and 5 simulation runs for a 2x2 Switch:
```bash
python src/Simulator.py --heuristic GLJD --size 3 --runs 5
```
* Get an explanation of a configuration parameters:
```bash
python src/Simulator.py --help
```
### Run simulation suite
To run the simulation suite with simulation runs for all possible configurations and save the results into a CSV file:
```bash
python src/Simulation_Suite.py
```
