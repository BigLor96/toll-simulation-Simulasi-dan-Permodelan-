"""Rush hour scenario: High arrival rate."""

from ..config import SIMULATION_TIME, DEFAULT_RANDOM_SEED
from ..simulation import run_simulation, SimulationMetrics


def run_rush_hour():
    """
    Run rush hour scenario with higher arrival rate.
    
    Returns:
        Tuple of (SimulationEnvironment, SimulationMetrics)
    """
    num_booths = 1  # same as baseline
    arrival_rate = 4.0  # cars per minute (double the baseline)
    service_time = 1.0  # minutes (same as baseline)
    
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
    sim_env, metrics = run_rush_hour()
    print("Rush Hour Scenario Results:")
    print(metrics.summary())
