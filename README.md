# SpaceSim

Synthetic spacecraft visualization & closed-loop GNC sandbox.

## Overview
This repository contains a minimal seed implementation (`space_sim_seed.py`) and
design documents for a modular simulation environment targeting synthetic
vision-based navigation near the Moon. The goal is to generate annotated frames
(RGB, depth, segmentation) while running a simplified guidance-navigation-
control loop.

## Architecture Diagram
```
+------------+       +-------------+        +------------+
| Dynamics   | ----> | Rendering   | ---->  | Navigation |
| Propagator |       | (Blender)   |        |  (EKF)     |
+------------+       +-------------+        +------------+
       ^                     |                     |
       |                     v                     |
       +--------------- Control <------------------+
```

Modules communicate via lightweight Python interfaces, enabling future backends
(e.g., Unity or Unreal) by swapping the rendering implementation.

## Quick Start
Run headless Blender with the seed script to generate 120 frames:
```bash
blender --background --python space_sim_seed.py
```
Outputs are written to `frames/` along with `log.csv` containing timestamps and
positions.

## Configuration
Simulation parameters (orbit radius, step size, lighting, etc.) can be adjusted
by editing constants at the top of `space_sim_seed.py`. Future versions will
load a YAML/JSON config file.

## Extending
- **Unity/Unreal**: Implement the same render interface in C# or C++ while
  preserving the data logging format.
- **Control**: Replace the placeholder controller with a two-burn-per-period
  MPC policy.
- **Navigation**: Swap the ground truth feed with a vision-based estimator.

## References
- Station-keeping MPC approaches (see research on NRHO targeting).
- Synthetic dataset generation and domain randomization literature.

## Reproducibility
Set the `SEED` constant in `space_sim_seed.py` to reproduce deterministic runs.
