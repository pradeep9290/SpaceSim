"""Minimal seed implementation for SpaceSim.

This script uses Blender's Python API (`bpy`) to create a simple scene with a
spacecraft sphere, a moon sphere, a sun lamp, and a camera. It propagates a
circular orbit and renders RGB and depth images for 120 frames. Results are
written to the `frames/` directory along with a CSV log of timestamps and
positions.

Run with:
    blender --background --python space_sim_seed.py
"""

import csv
import math
import os
import random
from typing import Tuple

try:
    import bpy
except ImportError:
    bpy = None  # Allows linting outside Blender

SEED = 42
NUM_FRAMES = 120
DT = 1.0  # seconds
ORBIT_RADIUS = 1000.0  # meters

random.seed(SEED)


def init_scene():
    """Create spacecraft, moon, lamp, and camera."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"

    # Moon
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1737.4, location=(0, 0, 0))
    moon = bpy.context.object
    moon.name = "Moon"

    # Spacecraft proxy
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(ORBIT_RADIUS, 0, 0))
    craft = bpy.context.object
    craft.name = "Spacecraft"

    # Sun lamp
    lamp_data = bpy.data.lights.new(name="Sun", type='SUN')
    lamp = bpy.data.objects.new(name="Sun", object_data=lamp_data)
    scene.collection.objects.link(lamp)
    lamp.rotation_euler = (math.radians(45), 0, 0)

    # Camera
    cam_data = bpy.data.cameras.new("Camera")
    cam = bpy.data.objects.new("Camera", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    return cam, craft


def propagate(theta: float) -> Tuple[float, float, float]:
    """Return spacecraft position on a circular orbit."""
    x = ORBIT_RADIUS * math.cos(theta)
    y = ORBIT_RADIUS * math.sin(theta)
    z = 0.0
    return x, y, z


def render_frame(frame: int, cam, craft, theta: float, log_writer):
    pos = propagate(theta)
    craft.location = pos
    cam.location = (pos[0], pos[1] - 10.0, pos[2] + 2.0)
    cam.rotation_euler = (math.radians(90), 0, theta + math.pi)
    bpy.context.scene.frame_set(frame)

    # Paths
    base = os.path.join("frames", f"frame_{frame:04d}")
    rgb_path = base + "_rgb.png"
    depth_path = base + "_depth.exr"

    bpy.context.scene.node_tree = None
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    tree.nodes.clear()

    rl = tree.nodes.new('CompositorNodeRLayers')
    comp = tree.nodes.new('CompositorNodeComposite')
    depth_file = tree.nodes.new('CompositorNodeOutputFile')
    depth_file.format.file_format = 'OPEN_EXR'
    depth_file.base_path = ''
    depth_file.file_slots[0].path = depth_path

    tree.links.new(rl.outputs['Depth'], depth_file.inputs[0])
    tree.links.new(rl.outputs['Image'], comp.inputs[0])

    bpy.context.scene.render.filepath = rgb_path
    bpy.ops.render.render(write_still=True)

    log_writer.writerow({'frame': frame, 'time': frame * DT,
                         'x': pos[0], 'y': pos[1], 'z': pos[2],
                         'rgb': rgb_path, 'depth': depth_path})


def estimate_state():
    """Placeholder state estimator."""
    pass


def compute_control():
    """Placeholder control law."""
    pass


def main():
    if bpy is None:
        raise RuntimeError("This script must run inside Blender")

    os.makedirs('frames', exist_ok=True)
    cam, craft = init_scene()

    with open('log.csv', 'w', newline='') as csvfile:
        fieldnames = ['frame', 'time', 'x', 'y', 'z', 'rgb', 'depth']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        theta = 0.0
        for frame in range(NUM_FRAMES):
            render_frame(frame, cam, craft, theta, writer)
            theta += DT * math.sqrt(398600.0 / ORBIT_RADIUS ** 3)  # Keplerian

            estimate_state()  # no-op
            compute_control()  # no-op

if __name__ == "__main__":
    main()
