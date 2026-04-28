"""Baseline scenario: 1 booth, default parameters."""

from ..config import SIMULATION_TIME, DEFAULT_RANDOM_SEED
from ..simulation import run_simulation, SimulationMetrics


def run_baseline():
    """
    Run baseline scenario.
    
    Returns:
        Tuple of (SimulationEnvironment, SimulationMetrics)
    """
    num_booths = 1
    arrival_rate = 2.0  # cars per minute
    service_time = 1.0  # minutes
    
    sim_env = run_simulation(
        num_booths=num_booths,
        arrival_rate=arrival_rate,
        service_time=service_time,
        simulation_time=SIMULATION_TIME,
        random_seed=DEFAULT_RANDOM_SEED
    )
    
    metrics = SimulationMetrics(sim_env)
    
    return sim_env, metrics


if __name__ == "__main__":
    sim_env, metrics = run_baseline()
    print("Baseline Scenario Results:")
    print(metrics.summary())
