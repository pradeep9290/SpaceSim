# Control Loop Pseudocode

```python
class State:
    position: np.ndarray  # 3-vector in meters
    velocity: np.ndarray  # 3-vector in m/s

class ControlCommand:
    dv: np.ndarray  # impulsive delta-V in m/s

class RenderedFrame:
    rgb_path: str
    depth_path: str
    seg_path: str
    normal_path: str
```

## Main Loop
```python
state = initial_state()
for t in range(N):
    state = propagate(state, dt)
    render(state)  # saves RGB, depth, seg, normal
    estimate = estimate_state()  # placeholder EKF
    cmd = compute_control(state, estimate)
    state = apply_control(state, cmd)
    log(state, estimate, cmd)
```
