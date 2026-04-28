"""Three booths scenario: 3 booths with same arrival and service rates."""

from ..config import SIMULATION_TIME, DEFAULT_RANDOM_SEED
from ..simulation import run_simulation, SimulationMetrics


def run_three_booths():
    """
    Run three booths scenario.
    
    Returns:
        Tuple of (SimulationEnvironment, SimulationMetrics)
    """
    num_booths = 3
    arrival_rate = 2.0  # cars per minute (same as baseline)
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
    sim_env, metrics = run_three_booths()
    print("Three Booths Scenario Results:")
    print(metrics.summary())
