"""Toll gate operations and processes."""

import simpy
from .car import Car
from .env import SimulationEnvironment


def car_process(env: SimulationEnvironment, car_id, arrival_time, service_time):
    """
    Simulate a car's journey through the toll gate.
    
    Args:
        env: SimulationEnvironment instance
        car_id: Unique car identifier
        arrival_time: Car's arrival time
        service_time: Service duration at booth
    """
    car = Car(car_id, arrival_time)
    
    # Car arrives at toll gate
    yield env.env.timeout(arrival_time)
    env.record_event('arrive', car_id, {'time': env.env.now})
    
    # Request a booth
    with env.toll_booths.request() as req:
        # Wait for booth availability
        yield req
        car.service_start_time = env.env.now
        env.record_waiting_time(car.waiting_time)
        env.record_event('start_service', car_id, {'wait_time': car.waiting_time})
        
        # Get service
        yield env.env.timeout(service_time)
        car.departure_time = env.env.now
        env.record_event('depart', car_id, {'time': env.env.now})
    
    env.cars_served += 1


def car_generator(env: SimulationEnvironment, service_time, simulation_time):
    """
    Generate cars with exponential inter-arrival times.
    
    Args:
        env: SimulationEnvironment instance
        service_time: Service duration at booth
        simulation_time: Total simulation duration
    """
    car_id = 0
    current_time = 0
    
    while current_time < simulation_time:
        inter_arrival = env.get_inter_arrival_time()
        current_time += inter_arrival
        
        if current_time < simulation_time:
            env.env.process(
                car_process(env, car_id, current_time, service_time)
            )
            car_id += 1
        
        yield env.env.timeout(inter_arrival)


def queue_monitor(env: SimulationEnvironment, simulation_time):
    """
    Monitor queue length over time at regular intervals.
    
    Args:
        env: SimulationEnvironment instance
        simulation_time: Total simulation duration
    """
    from ..config import QUEUE_SAMPLE_INTERVAL
    
    while env.env.now < simulation_time:
        queue_length = len(env.toll_booths.queue)
        env.record_queue_state(env.env.now, queue_length)
        yield env.env.timeout(QUEUE_SAMPLE_INTERVAL)


def run_simulation(num_booths, arrival_rate, service_time, simulation_time, random_seed=None):
    """
    Run a complete toll gate simulation.
    
    Args:
        num_booths: Number of toll booths
        arrival_rate: Cars per minute
        service_time: Service time per car
        simulation_time: Simulation duration in minutes
        random_seed: Random seed for reproducibility
    
    Returns:
        SimulationEnvironment with recorded metrics
    """
    env = SimulationEnvironment(num_booths, arrival_rate, service_time, random_seed)
    
    # Start processes
    env.env.process(car_generator(env, service_time, simulation_time))
    env.env.process(queue_monitor(env, simulation_time))
    
    # Run simulation
    env.env.run()
    
    return env
