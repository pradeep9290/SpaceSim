# System Architecture

This document sketches the high level design of the SpaceSim environment.

```
+-----------+     +------------+     +-------------+     +----------+
| Dynamics  | --> | Rendering  | --> | Navigation   | --> | Control  |
| Propagator|     | (Backend)  |     | (EKF/MPC)    |     | Policy   |
+-----------+     +------------+     +-------------+     +----------+
       ^                                                    |
       +----------------------------------------------------+
```

## Modules
- **Dynamics**: Integrates the spacecraft state using a CR3BP or simplified two-body model.
- **Rendering**: Backend-agnostic interface. Initial implementation uses Blender
  (`bpy`) to generate RGB, depth, segmentation, and normals with optional domain
  randomization.
- **Navigation**: Placeholder EKF that ingests either ground truth or synthetic
  imagery.
- **Control**: Two-burn-per-period MPC-inspired policy producing thrust commands.
- **Data Logging**: Records per-frame state, estimated state, and file paths to
  rendered outputs.

Future backends (Unity, Unreal) should implement the same rendering interface to
plug into the loop.
