"""Visualization plots for simulation results."""

import matplotlib.pyplot as plt


def plot_queue_length(sim_env, title="Queue Length Over Time"):
    """
    Plot queue length over time.
    
    Args:
        sim_env: SimulationEnvironment with recorded data
        title: Plot title
    """
    plt.figure(figsize=(10, 6))
    plt.plot(sim_env.queue_timestamps, sim_env.queue_lengths, 
             linewidth=2, color='steelblue', marker='o', markersize=3, alpha=0.7)
    plt.xlabel("Time (minutes)", fontsize=12)
    plt.ylabel("Queue Length", fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt.gcf()


def plot_scenario_comparison(scenarios_data):
    """
    Compare average waiting times across scenarios.
    
    Args:
        scenarios_data: Dict mapping scenario name to metrics
    
    Example:
        scenarios_data = {
            "Baseline": metrics1,
            "Three Booths": metrics2,
            ...
        }
    """
    scenario_names = list(scenarios_data.keys())
    avg_waiting_times = [scenarios_data[name].avg_waiting_time for name in scenario_names]
    max_waiting_times = [scenarios_data[name].max_waiting_time for name in scenario_names]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Average waiting time
    colors = ['#ff7f0e', '#2ca02c', '#1f77b4', '#d62728']
    ax1.bar(scenario_names, avg_waiting_times, color=colors[:len(scenario_names)], alpha=0.8)
    ax1.set_ylabel("Average Waiting Time (minutes)", fontsize=11)
    ax1.set_title("Average Waiting Time by Scenario", fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(avg_waiting_times):
        ax1.text(i, v + 0.05, f'{v:.2f}', ha='center', fontsize=10)
    
    # Max waiting time
    ax2.bar(scenario_names, max_waiting_times, color=colors[:len(scenario_names)], alpha=0.8)
    ax2.set_ylabel("Maximum Waiting Time (minutes)", fontsize=11)
    ax2.set_title("Maximum Waiting Time by Scenario", fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(max_waiting_times):
        ax2.text(i, v + 0.1, f'{v:.2f}', ha='center', fontsize=10)
    
    plt.tight_layout()
    return fig


def plot_all_queue_lengths(scenarios_data):
    """
    Plot queue lengths for all scenarios on same plot for comparison.
    
    Args:
        scenarios_data: Dict mapping scenario name to SimulationEnvironment
    """
    plt.figure(figsize=(12, 6))
    
    colors = ['#ff7f0e', '#2ca02c', '#1f77b4', '#d62728']
    for (name, sim_env), color in zip(scenarios_data.items(), colors):
        plt.plot(sim_env.queue_timestamps, sim_env.queue_lengths, 
                 label=name, linewidth=2, color=color, alpha=0.7)
    
    plt.xlabel("Time (minutes)", fontsize=12)
    plt.ylabel("Queue Length", fontsize=12)
    plt.title("Queue Length Comparison Across Scenarios", fontsize=14, fontweight='bold')
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt.gcf()
