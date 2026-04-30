Behind-the-scenes evidence
# Development Notes – Swarm Intelligence Simulation Project

This document records key technical decisions, system changes, debugging additions, and implementation milestones throughout the project.

---

## Project Purpose

The aim of this project is to develop and evaluate a multi-agent swarm simulation system that compares centralised, decentralised, hybrid, and random coordination strategies under different operating and failure conditions.

---

## Initial Simulation Setup

### Grid Environment Created
- Built a 2D grid simulation environment.
- Agents move across the grid and mark visited cells.

### Agent Movement Implemented
Initial movement model:
- Random movement only.

Purpose:
- Establish baseline benchmark for comparison.

---

## Reproducibility Control Added

### Random Seed Implemented

Code added:
```python
random.seed(42)
np.random.seed(42)
### Purpose:

Ensure simulation results are repeatable.
Maintain fair comparison across strategy tests.

Reason:
Without fixed seeds, graphs changed every run due to randomness.
Strategy Implementations

##1. Random Strategy

## Purpose:

Baseline comparison model.
Represents no intelligent coordination.

##2. Decentralised Strategy

##Purpose:

Agents prioritise nearby unvisited cells.
Simulates swarm-like local decision making.

Key Observation:

Strong performance improvement over random.

3##. Centralised Strategy

##Purpose:

One controller assigns nearest unvisited targets.
Key Observation:
Better than random, weaker than decentralised.

##4. Hybrid Strategy

##Purpose:

Combine decentralised local exploration with centralised fallback guidance.

Key Observation:

Best overall performance under normal conditions.
