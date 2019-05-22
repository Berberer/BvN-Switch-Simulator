import simpy
from Traffic_Generator import Traffic_Generator
from Switch import Switch
from Schedule import Schedule

# TODO: Replace hard-coded matrix with a automatically created one
traffic_matrix = [
    [0.5, 0.5],
    [0.5, 0.5]
]

env = simpy.Environment()
traffic_generator = Traffic_Generator(traffic_matrix)
# TODO: Create actual matrices and probabilities for the schedule with BvN
permutation_matrices = [
    [[1,0],[0,1]],
    [[0,1],[1,0]]
]
probabilities = [0.5, 0.5]
schedule = Schedule(permutation_matrices,probabilities)
switch = Switch(2, 2, schedule)

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

env.process(traffic_generation_step(env, 1))
env.process(switch_forwarding_step(env, 2))

env.run(until=10)
