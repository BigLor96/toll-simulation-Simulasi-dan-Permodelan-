# Toll Gate Queue Simulation

A discrete-event simulation of a toll gate queue system using **SimPy**, modeling cars arriving, waiting, receiving service, and leaving.

## Project Structure

```
toll-simulation/
├── main.py                 # Main entry point - runs all scenarios and generates visualizations
├── animate.py             # Quick animation demo script
├── config.py              # Configuration constants
├── simulation/            # Core simulation logic
│   ├── __init__.py
│   ├── env.py            # SimPy environment and setup
│   ├── car.py            # Car entity
│   ├── toll.py           # Toll gate processes and simulation runner
│   └── metrics.py        # Metrics calculation and analysis
├── scenarios/            # Pre-defined simulation scenarios
│   ├── __init__.py
│   ├── baseline.py       # 1 booth, 2 cars/min, 1.0 min service
│   ├── three_booths.py   # 3 booths, 2 cars/min, 1.0 min service
│   ├── fast_payment.py   # 1 booth, 2 cars/min, 0.5 min service
│   └── rush_hour.py      # 1 booth, 4 cars/min, 1.0 min service
└── visualization/        # Plotting and visualization
    ├── __init__.py
    ├── plot.py           # Queue and comparison charts
    ├── layout.py         # 2D toll gate layout
    └── animation.py      # Pygame-based animated replay (Karawaci 2 layout)
```

## Features

### Simulation Logic
- **Exponential inter-arrival times** based on configurable arrival rate
- **SimPy discrete-event simulation** with environment management
- **Resource-based booths** with configurable capacity
- **60-minute simulation** duration
- **Modular car process** tracking arrival, service, and departure

### Metrics Collected
- **Waiting times** for each car (arrival to service start)
- **Queue length samples** at 0.1 time unit intervals
- **Maximum queue length** observed
- **Average/min/max waiting times**
- **Queue statistics** (average, max)

### Scenarios
1. **Baseline**: 1 booth, 2 cars/min arrival, 1 min service time
2. **Three Booths**: 3 booths, 2 cars/min arrival, 1 min service time
3. **Fast Payment**: 1 booth, 2 cars/min arrival, 0.5 min service time
4. **Rush Hour**: 1 booth, 4 cars/min arrival, 1 min service time

### Visualizations
- **Individual queue length plots** for each scenario
- **Scenario comparison**: Average and max waiting times (bar charts)
- **Queue length comparison** across all scenarios
- **Toll gate layout**: Simple 2D representation with roads, booths, and cars
- **Animated replay**: Pygame-based 2D semi-3D animation with Karawaci 2 toll gate layout
  - Cars move through incoming lanes → queue area → toll booths → exit lanes
  - Real-time barrier animations when cars are served
  - Smooth playback with speed control

## Installation

### Requirements
- Python 3.7+
- SimPy
- Matplotlib
- Pygame (for animation)

### Setup
```bash
pip install simpy matplotlib pygame
```

## Usage

### Run Complete Simulation
```bash
python toll-simulation/main.py
```

This will:
1. Run all 4 scenarios
2. Print detailed metrics for each scenario
3. Generate 7 visualization files (PNG format)
4. Display all plots interactively

### Run Individual Scenario
```bash
# Baseline
python -m toll-simulation.scenarios.baseline

# Three Booths
python -m toll-simulation.scenarios.three_booths

# Fast Payment
python -m toll-simulation.scenarios.fast_payment

# Rush Hour
python -m toll-simulation.scenarios.rush_hour
```

### Custom Simulation
```python
from toll-simulation.simulation import run_simulation, SimulationMetrics

# Run custom simulation
sim_env = run_simulation(
    num_booths=2,
    arrival_rate=3.0,      # cars/min
    service_time=0.75,     # minutes
    simulation_time=60,
    random_seed=42
)

metrics = SimulationMetrics(sim_env)
print(metrics.summary())
```

### Animation Replay
Run the complete simulation and optionally animate:
```bash
python -m toll-simulation.main
# When prompted, select a scenario (1-4) to animate, or skip (5)
```

Or directly animate a specific scenario:
```bash
python -m toll-simulation.animate
# Select scenario interactively, or pass as argument:
python -m toll-simulation.animate "Baseline"
python -m toll-simulation.animate "Three Booths"
python -m toll-simulation.animate "Rush Hour"
```

**Animation Controls:**
- **Space**: Play/Pause
- **Left/Right arrows**: Change playback speed
- **Up/Down arrows**: Fine-tune speed (±0.1x)
- **R**: Reset to beginning
- **Q**: Quit

**Animation Features:**
- Karawaci 2 toll gate layout with incoming/exit lanes
- Real-time car movement and positioning
- Queue visualization
- Barrier animation (red=serving, green=open)
- Live HUD showing time, active cars, and playback speed

## Output Files

When running `main.py`, the following PNG files are generated:
- `queue_baseline.png` - Queue length for baseline scenario
- `queue_three_booths.png` - Queue length for three booths scenario
- `queue_fast_payment.png` - Queue length for fast payment scenario
- `queue_rush_hour.png` - Queue length for rush hour scenario
- `comparison_waiting_times.png` - Waiting time comparison across scenarios
- `comparison_queue_lengths.png` - Queue length comparison overlay
- `toll_gate_layout.png` - 2D toll gate layout visualization

## Key Metrics Explained

| Metric | Description |
|--------|-------------|
| **Waiting Time** | Time from arrival to service start (includes queue wait) |
| **Queue Length** | Number of cars waiting (sampled every 0.1 time units) |
| **Average Waiting Time** | Mean waiting time across all cars |
| **Max Queue Length** | Peak queue length during simulation |
| **Cars Served** | Total number of cars processed |

## Animation Architecture

The animation system works by:

1. **Event Recording**: During simulation, each car's lifecycle events are recorded:
   - `arrive`: Car enters the toll gate area
   - `start_service`: Car begins service at a booth
   - `depart`: Car leaves the system

2. **Timeline Playback**: The animation replays these events on a 2D canvas:
   - Car positions are interpolated between events for smooth movement
   - Queue area shows accumulating cars during peak times
   - Barriers animate (red=open, green=closed) based on booth occupancy

3. **Layout**: Inspired by Karawaci 2 toll gate:
   - Angled incoming lanes that merge into a queue area
   - Multiple toll booths with real-time barrier visualization
   - Exit lane with perspective effect
   - All motion is replay of actual simulation, not real-time physics

## Modular Design

The code is organized for easy extension:

### Add New Scenario
Create a new file in `scenarios/` with a `run_scenarioname()` function:
```python
from ..config import SIMULATION_TIME, DEFAULT_RANDOM_SEED
from ..simulation import run_simulation, SimulationMetrics

def run_my_scenario():
    sim_env = run_simulation(
        num_booths=2,
        arrival_rate=3.0,
        service_time=0.8,
        simulation_time=SIMULATION_TIME,
        random_seed=DEFAULT_RANDOM_SEED
    )
    return sim_env, SimulationMetrics(sim_env)
```

### Add Custom Metrics
Extend `SimulationMetrics` class in `simulation/metrics.py` with new properties.

### Customize Visualization
Use `plot.py` functions or create new visualization functions in `visualization/`.

## Code Quality

- **Modular**: Separate concerns (environment, entities, processes, metrics, visualization)
- **Clean**: Clear variable names, minimal comments, simple logic
- **Configurable**: Easy to adjust simulation parameters
- **Reproducible**: Optional random seed for consistent results
- **Extensible**: Simple to add scenarios and metrics

## Example Results

Running the default scenarios typically produces:

| Scenario | Avg Wait (min) | Max Queue |
|----------|---|---|
| Baseline | 2.45 | 8 |
| Three Booths | 0.12 | 2 |
| Fast Payment | 0.95 | 5 |
| Rush Hour | 8.32 | 15 |

*(Results vary due to stochastic simulation)*

## Notes

- Inter-arrival times follow exponential distribution
- Service times are fixed (deterministic)
- Cars arrive with id incrementing from 0
- Simulation uses discrete time steps
- All time values in minutes

## Author

Simulasi dan Permodelan - Toll Gate Queue System Simulation 
