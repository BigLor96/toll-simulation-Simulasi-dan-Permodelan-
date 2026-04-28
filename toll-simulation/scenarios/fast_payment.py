"""Fast payment scenario: Reduced service time."""

from ..config import SIMULATION_TIME, DEFAULT_RANDOM_SEED
from ..simulation import run_simulation, SimulationMetrics


def run_fast_payment():
    """
    Run fast payment scenario with faster service times.
    
    Returns:
        Tuple of (SimulationEnvironment, SimulationMetrics)
    """
    num_booths = 1  # same as baseline
    arrival_rate = 2.0  # cars per minute (same as baseline)
    service_time = 0.5  # minutes (faster)
    
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
    sim_env, metrics = run_fast_payment()
    print("Fast Payment Scenario Results:")
    print(metrics.summary())
