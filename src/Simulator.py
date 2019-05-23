import simpy
import sys
import numpy as np
from Traffic_Generator import Traffic_Generator
from Switch import Switch
from Schedule import Schedule
from Decomposition_Algorithms import gljd

# TODO: Add the remaining heuristics
heuristics = {
    "GLJD": gljd
}

def traffic_generation_step(env, tick):
    while True:
        generated_packets = traffic_generator.generate_packets(tick)
        switch.packets_arrive(generated_packets)
        print("Generated traffic in step {}: {}".format(
            tick, ', '.join(str(x) for x in generated_packets)
            )
        )
        yield env.timeout(tick)

def switch_forwarding_step(env, tick):
    while True:
        print("Forwarding:")
        switch.forward_packets()
        yield env.timeout(tick)

if len(sys.argv) < 2:
    print("Parameter missing: HEURISTIC")
else:
    selected_heuristic = sys.argv[1]
    if selected_heuristic.upper() in heuristics:
        # TODO: Replace hard-coded matrix with a automatically created one
        traffic_matrix = np.array([
            [0.38, 0, 0.22, 0.4],
            [0.11, 0.24, 0.6, 0.05],
            [0, 0.53, 0.14, 0.33],
            [0.51, 0.23, 0.04, 0.22]
        ])
        env = simpy.Environment()
        traffic_generator = Traffic_Generator(traffic_matrix)
        permutation_matrices, probabilities = heuristics[selected_heuristic.upper()](traffic_matrix)
        schedule = Schedule(permutation_matrices,probabilities)
        switch = Switch(traffic_matrix.shape[0], traffic_matrix.shape[1], schedule)
        env.process(traffic_generation_step(env, 1))
        env.process(switch_forwarding_step(env, 2))
        env.run(until=10)
    else:
        print("Unknown heuristic {}. Simulation cannot be started".format(selected_heuristic))
