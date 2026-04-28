"""Metrics analysis for simulation results."""

from statistics import mean, stdev


class SimulationMetrics:
    """Calculate and store simulation metrics."""
    
    def __init__(self, sim_env):
        """
        Initialize metrics from simulation environment.
        
        Args:
            sim_env: SimulationEnvironment with recorded data
        """
        self.sim_env = sim_env
        self.waiting_times = sim_env.waiting_times
        self.queue_lengths = sim_env.queue_lengths
        self.queue_timestamps = sim_env.queue_timestamps
        self.cars_served = sim_env.cars_served
    
    @property
    def avg_waiting_time(self):
        """Average waiting time across all cars."""
        if not self.waiting_times:
            return 0
        return mean(self.waiting_times)
    
    @property
    def max_waiting_time(self):
        """Maximum waiting time."""
        if not self.waiting_times:
            return 0
        return max(self.waiting_times)
    
    @property
    def min_waiting_time(self):
        """Minimum waiting time."""
        if not self.waiting_times:
            return 0
        return min(self.waiting_times)
    
    @property
    def std_waiting_time(self):
        """Standard deviation of waiting times."""
        if len(self.waiting_times) < 2:
            return 0
        return stdev(self.waiting_times)
    
    @property
    def avg_queue_length(self):
        """Average queue length."""
        if not self.queue_lengths:
            return 0
        return mean(self.queue_lengths)
    
    @property
    def max_queue_length(self):
        """Maximum queue length observed."""
        if not self.queue_lengths:
            return 0
        return max(self.queue_lengths)
    
    def summary(self):
        """Get summary of all metrics."""
        return {
            "cars_served": self.cars_served,
            "avg_waiting_time": round(self.avg_waiting_time, 4),
            "max_waiting_time": round(self.max_waiting_time, 4),
            "min_waiting_time": round(self.min_waiting_time, 4),
            "std_waiting_time": round(self.std_waiting_time, 4),
            "avg_queue_length": round(self.avg_queue_length, 4),
            "max_queue_length": self.max_queue_length,
        }
