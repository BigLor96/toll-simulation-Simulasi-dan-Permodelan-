"""Simulation environment setup."""

import simpy
import random


class SimulationEnvironment:
    """Wrapper for SimPy environment and toll gate setup."""
    
    def __init__(self, num_booths, arrival_rate, service_time, random_seed=None):
        """
        Initialize simulation environment.
        
        Args:
            num_booths: Number of toll booths
            arrival_rate: Cars arriving per minute
            service_time: Service time per car in minutes
            random_seed: Random seed for reproducibility
        """
        if random_seed is not None:
            random.seed(random_seed)
        
        self.env = simpy.Environment()
        self.num_booths = num_booths
        self.arrival_rate = arrival_rate
        self.service_time = service_time
        self.random_seed = random_seed
        
        # Create toll booth resource
        self.toll_booths = simpy.Resource(self.env, capacity=num_booths)
        
        # Metrics tracking
        self.cars_served = 0
        self.waiting_times = []
        self.queue_lengths = []
        self.queue_timestamps = []
        
        # Timeline events for animation
        self.timeline = []  # List of (time, event_type, car_id, data)
        self.car_states = {}  # Track car states for animation
    
    def get_inter_arrival_time(self):
        """Generate exponential inter-arrival time based on arrival rate."""
        return random.expovariate(self.arrival_rate)
    
    def record_waiting_time(self, wait_time):
        """Record a car's waiting time."""
        self.waiting_times.append(wait_time)
    
    def record_queue_state(self, timestamp, queue_length):
        """Record queue length at a specific timestamp."""
        self.queue_timestamps.append(timestamp)
        self.queue_lengths.append(queue_length)
    
    def record_event(self, event_type, car_id, data=None):
        """Record a timeline event for animation."""
        self.timeline.append({
            'time': self.env.now,
            'type': event_type,
            'car_id': car_id,
            'data': data or {}
        })
