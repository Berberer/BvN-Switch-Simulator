# BvN-Switch-Simulator

Simluator for Birkhoff–von Neumann scheduling in a switch. Different heuristics for the scheduling are compared regarding metrics like packet delay, queue size, throughput, etc.

## Getting Started
### Install dependencies:
```bash
pip install -r requirements.txt
```
### Run simulations
* Run the simulator and select your simulation configuration interactively:
```bash
python src/Simulator.py
```
* Specify your configuration manually. For example in the case of GLJD and 5 simulation runs:
```bash
python src/Simulator.py --heuristic GLJD --runs 5
```
* Get an explanation of a configuration parameters:
```bash
python src/Simulator.py --help
```
