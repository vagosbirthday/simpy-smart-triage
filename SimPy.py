import simpy
import random
import statistics

LAMBDA = 0.10
MU = 0.125
SIM_TIME = 50000   
WARMUP = 1000      

waiting_times = []
system_times = []
queue_lengths = []

def patient(env, name, server):
    arrival_time = env.now

    with server.request() as request:
        yield request

        wait = env.now - arrival_time
        waiting_times.append(wait)

        service_time = random.expovariate(MU)
        yield env.timeout(service_time)

        total_time = env.now - arrival_time
        system_times.append(total_time)

def arrival_process(env, server):
    i = 0
    while True:
        i += 1
        yield env.timeout(random.expovariate(LAMBDA))
        env.process(patient(env, f"Paciente {i}", server))
        queue_lengths.append(len(server.queue))

env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

env.process(arrival_process(env, server))
env.run(until=SIM_TIME)

waiting_times = waiting_times[WARMUP:]
system_times = system_times[WARMUP:]
queue_lengths = queue_lengths[WARMUP:]

print("\nResultados de la simulación (estado estable):\n")
print(f"Pacientes atendidos: {len(system_times)}")
print(f"Wq (cola): {statistics.mean(waiting_times):.2f} min")
print(f"Ws (sistema): {statistics.mean(system_times):.2f} min")
print(f"Lq (cola): {statistics.mean(queue_lengths):.2f} pacientes")