"""Quick animation demo - run a specific scenario and animate it."""

import sys
from .simulation import run_simulation, SimulationMetrics
from .visualization import animate_scenario
from .config import SIMULATION_TIME, DEFAULT_RANDOM_SEED


def run_scenario_animation(scenario_name="Baseline"):
    """
    Run a scenario and show animation.
    
    Args:
        scenario_name: Name of scenario (Baseline, Three Booths, Fast Payment, Rush Hour)
    """
    
    print(f"Setting up {scenario_name} scenario...")
    
    # Scenario parameters
    scenarios = {
        "Baseline": {
            "num_booths": 1,
            "arrival_rate": 2.0,
            "service_time": 1.0,
        },
        "Three Booths": {
            "num_booths": 3,
            "arrival_rate": 2.0,
            "service_time": 1.0,
        },
        "Fast Payment": {
            "num_booths": 1,
            "arrival_rate": 2.0,
            "service_time": 0.5,
        },
        "Rush Hour": {
            "num_booths": 1,
            "arrival_rate": 4.0,
            "service_time": 1.0,
        },
    }
    
    if scenario_name not in scenarios:
        print(f"Unknown scenario: {scenario_name}")
        print(f"Available: {', '.join(scenarios.keys())}")
        return
    
    params = scenarios[scenario_name]
    
    print(f"Running simulation...")
    sim_env = run_simulation(
        num_booths=params["num_booths"],
        arrival_rate=params["arrival_rate"],
        service_time=params["service_time"],
        simulation_time=SIMULATION_TIME,
        random_seed=DEFAULT_RANDOM_SEED
    )
    
    metrics = SimulationMetrics(sim_env)
    
    print(f"\nSimulation Results:")
    print(f"  Cars served: {metrics.cars_served}")
    print(f"  Avg waiting time: {metrics.avg_waiting_time:.4f} min")
    print(f"  Max queue length: {metrics.max_queue_length}")
    
    print(f"\nStarting animation (close window to exit)...")
    print(f"Controls: Space=Play/Pause | Left/Right=Speed | Up/Down=Adjust | R=Reset | Q=Quit")
    
    animate_scenario(sim_env, num_booths=params["num_booths"], 
                    simulation_duration=SIMULATION_TIME)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        scenario = sys.argv[1]
    else:
        print("Toll Gate Animation Demo")
        print("\nAvailable scenarios:")
        print("  1. Baseline (1 booth)")
        print("  2. Three Booths (3 booths)")
        print("  3. Fast Payment (0.5 min service)")
        print("  4. Rush Hour (4 cars/min)")
        
        choice = input("\nSelect scenario (1-4) [default: 1]: ").strip() or "1"
        scenarios_list = ["Baseline", "Three Booths", "Fast Payment", "Rush Hour"]
        
        try:
            idx = int(choice) - 1
            scenario = scenarios_list[idx]
        except (ValueError, IndexError):
            print("Invalid choice, using Baseline")
            scenario = "Baseline"
    
    run_scenario_animation(scenario)
