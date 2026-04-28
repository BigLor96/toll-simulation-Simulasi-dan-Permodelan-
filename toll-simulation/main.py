"""Main simulation runner."""

import matplotlib.pyplot as plt
import sys
from .scenarios import run_baseline, run_three_booths, run_fast_payment, run_rush_hour
from .simulation import SimulationMetrics
from .visualization import (
    plot_queue_length, 
    plot_scenario_comparison, 
    plot_all_queue_lengths,
    draw_toll_gate_layout,
    animate_scenario
)


def main():
    """Run all scenarios and generate visualizations."""
    
    print("=" * 60)
    print("TOLL GATE QUEUE SIMULATION")
    print("=" * 60)
    
    # Run all scenarios
    print("\n[1/4] Running Baseline scenario...")
    baseline_env, baseline_metrics = run_baseline()
    print(f"    - Cars served: {baseline_metrics.cars_served}")
    print(f"    - Avg waiting time: {baseline_metrics.avg_waiting_time:.4f} min")
    
    print("\n[2/4] Running Three Booths scenario...")
    three_booths_env, three_booths_metrics = run_three_booths()
    print(f"    - Cars served: {three_booths_metrics.cars_served}")
    print(f"    - Avg waiting time: {three_booths_metrics.avg_waiting_time:.4f} min")
    
    print("\n[3/4] Running Fast Payment scenario...")
    fast_payment_env, fast_payment_metrics = run_fast_payment()
    print(f"    - Cars served: {fast_payment_metrics.cars_served}")
    print(f"    - Avg waiting time: {fast_payment_metrics.avg_waiting_time:.4f} min")
    
    print("\n[4/4] Running Rush Hour scenario...")
    rush_hour_env, rush_hour_metrics = run_rush_hour()
    print(f"    - Cars served: {rush_hour_metrics.cars_served}")
    print(f"    - Avg waiting time: {rush_hour_metrics.avg_waiting_time:.4f} min")
    
    # Print detailed metrics
    print("\n" + "=" * 60)
    print("DETAILED METRICS")
    print("=" * 60)
    
    scenarios = {
        "Baseline": baseline_metrics,
        "Three Booths": three_booths_metrics,
        "Fast Payment": fast_payment_metrics,
        "Rush Hour": rush_hour_metrics,
    }
    
    scenario_envs = {
        "Baseline": (baseline_env, 1),
        "Three Booths": (three_booths_env, 3),
        "Fast Payment": (fast_payment_env, 1),
        "Rush Hour": (rush_hour_env, 1),
    }
    
    for name, metrics in scenarios.items():
        print(f"\n{name}:")
        summary = metrics.summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")
    
    # Generate visualizations
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    # Individual queue length plots
    print("\nGenerating individual queue length plots...")
    plot_queue_length(baseline_env, "Baseline - Queue Length Over Time")
    plt.savefig("queue_baseline.png", dpi=100, bbox_inches='tight')
    
    plot_queue_length(three_booths_env, "Three Booths - Queue Length Over Time")
    plt.savefig("queue_three_booths.png", dpi=100, bbox_inches='tight')
    
    plot_queue_length(fast_payment_env, "Fast Payment - Queue Length Over Time")
    plt.savefig("queue_fast_payment.png", dpi=100, bbox_inches='tight')
    
    plot_queue_length(rush_hour_env, "Rush Hour - Queue Length Over Time")
    plt.savefig("queue_rush_hour.png", dpi=100, bbox_inches='tight')
    
    # Comparison plots
    print("Generating scenario comparison plots...")
    plot_scenario_comparison(scenarios)
    plt.savefig("comparison_waiting_times.png", dpi=100, bbox_inches='tight')
    
    # All queue lengths comparison
    print("Generating queue length comparison plot...")
    sim_envs = {
        "Baseline": baseline_env,
        "Three Booths": three_booths_env,
        "Fast Payment": fast_payment_env,
        "Rush Hour": rush_hour_env,
    }
    plot_all_queue_lengths(sim_envs)
    plt.savefig("comparison_queue_lengths.png", dpi=100, bbox_inches='tight')
    
    # Layout visualization
    print("Generating toll gate layout visualization...")
    draw_toll_gate_layout(num_booths=3, queue_length=5)
    plt.savefig("toll_gate_layout.png", dpi=100, bbox_inches='tight')
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - queue_baseline.png")
    print("  - queue_three_booths.png")
    print("  - queue_fast_payment.png")
    print("  - queue_rush_hour.png")
    print("  - comparison_waiting_times.png")
    print("  - comparison_queue_lengths.png")
    print("  - toll_gate_layout.png")
    
    # Animation playback option
    print("\n" + "=" * 60)
    print("ANIMATION PLAYBACK")
    print("=" * 60)
    print("\nAvailable scenarios for animation:")
    print("  1. Baseline")
    print("  2. Three Booths")
    print("  3. Fast Payment")
    print("  4. Rush Hour")
    print("  5. Skip animation")
    
    choice = input("\nSelect scenario to animate (1-5) [default: 5]: ").strip() or "5"
    
    if choice in ["1", "2", "3", "4"]:
        scenario_names = ["Baseline", "Three Booths", "Fast Payment", "Rush Hour"]
        selected_scenario = scenario_names[int(choice) - 1]
        print(f"\nAnimating {selected_scenario} scenario...")
        print("Loading pygame (this may take a moment)...")
        
        try:
            import pygame
            sim_env, num_booths = scenario_envs[selected_scenario]
            animate_scenario(sim_env, num_booths=num_booths, simulation_duration=60)
        except ImportError:
            print("ERROR: pygame is not installed.")
            print("Install it with: pip install pygame")
        except Exception as e:
            print(f"ERROR during animation: {e}")
    else:
        print("\nSkipping animation.")
    
    # Show all plots
    plt.show()


if __name__ == "__main__":
    main()
