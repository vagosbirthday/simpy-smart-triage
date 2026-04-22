import simpy
import random
import statistics

lmbda = 0.10
mu = 0.125
SIM_TIME = 10000

rho = lmbda / mu
P0 = 1 - rho
Ls = lmbda / (mu - lmbda)
Ws = 1 / (mu - lmbda)
Lq = (lmbda**2) / (mu * (mu - lmbda))
Wq = lmbda / (mu * (mu - lmbda))
Pn = (1 - rho) * (rho**3)

print("\n===== RESULTADOS TEÓRICOS (M/M/1) =====\n")
print(f"Utilización (rho): {rho:.2f}")
print(f"P0 (sistema vacío): {P0:.2f}")
print(f"Ls (clientes en sistema): {Ls:.2f}")
print(f"Ws (tiempo en sistema): {Ws:.2f} min")
print(f"Lq (clientes en cola): {Lq:.2f}")
print(f"Wq (tiempo en cola): {Wq:.2f} min")
print(f"P3 (3 pacientes): {Pn:.4f}")

wait_times = []
system_times = []
queue_lengths = []

def patient(env, server):
    arrival = env.now
    
    with server.request() as req:
        yield req
        
        wait = env.now - arrival
        wait_times.append(wait)
        
        service = random.expovariate(mu)
        yield env.timeout(service)
        
        total = env.now - arrival
        system_times.append(total)

def arrivals(env, server):
    while True:
        yield env.timeout(random.expovariate(lmbda))
        env.process(patient(env, server))
        queue_lengths.append(len(server.queue))

env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

env.process(arrivals(env, server))
env.run(until=SIM_TIME)

print("\n===== RESULTADOS DE SIMULACIÓN =====\n")
print(f"Pacientes atendidos: {len(system_times)}")
print(f"Wq (cola): {statistics.mean(wait_times):.2f} min")
print(f"Ws (sistema): {statistics.mean(system_times):.2f} min")
print(f"Lq (cola): {statistics.mean(queue_lengths):.2f} pacientes")