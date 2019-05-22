import simpy
from Traffic_Generator import Traffic_Generator

traffic_matrix = [
    [0.5, 0.4, 0.1],
    [0.2, 0.4, 0.1],
    [0.25, 0.25, 0.25],
    [0.4, 0.3, 0.2]
]

env = simpy.Environment()
traffic_generator = Traffic_Generator(traffic_matrix)

def traffic_generation_step(env, tick):
    while True:
        generated_packets = traffic_generator.generate_packets(tick)
        print("Generated traffic in step {}: {}".format(
            tick, ', '.join(str(x) for x in generated_packets)
            )
        )
        yield env.timeout(tick)

def switch_forwarding_step(env, tick):
    while True:
        print("Forward packets")
        yield env.timeout(tick)

env.process(traffic_generation_step(env, 1))
env.process(switch_forwarding_step(env, 1))

env.run(until=10)
