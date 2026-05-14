# Multi-Agent System FYP

## Project Overview

This project investigates adaptive coordination in multi-agent systems under failure conditions. The system simulates agents operating in a 2D grid environment and evaluates different coordination strategies, including random, centralised, decentralised, hybrid, and adaptive approaches.

The main aim is to explore how coordination strategies perform when agents fail, and whether an adaptive strategy selection mechanism can improve system response and resilience.

## Strategies Implemented

- Random strategy: baseline movement with no intelligent coordination.
- Centralised strategy: a controller assigns movement based on global grid information.
- Decentralised strategy: agents use local information to prioritise nearby unvisited cells.
- Hybrid strategy: combines decentralised local exploration with centralised fallback guidance.
- Adaptive strategy: switches between decentralised and hybrid strategies based on failure severity.

## Failure Simulation

Agent dropout is used to simulate system failure. Dropout levels tested include:

- 10%
- 30%
- 50%

## Tools Used

- Python
- VS Code
- NumPy
- Matplotlib
- Git and GitHub

## Project Structure

```text
src/        Source code
results/    CSV result files
docs/       Development notes and documentation
figures/    Graph screenshots and visual outputs