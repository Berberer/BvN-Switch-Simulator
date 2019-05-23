# BvN-Switch-Simulator

Simluator for Birkhoff–von Neumann scheduling in a switch. Different heuristics for the scheduling are compared regarding metrics like packet delay, queue size, throughput, etc.

## Getting Started
  1) Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  2) Run the simulator with the desired heuristic. For example in the case of GLJD :
  ```bash
  python src/Simulator.py gljd
  ```
