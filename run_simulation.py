import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import animation

# Parameters
N = 30                # Number of cars
T = 100               # Simulation time
dt = 0.1              # Time step
a = 1.0               # Sensitivity parameter
tau = 0.5             # Reaction delay (not explicitly used in Euler integration)
v_max = 2.0           # Maximum velocity
d_safe = 2.0          # Safe distance

# Optimal velocity function (realistic model)
def V(delta_x):
    return v_max * np.tanh(delta_x - d_safe) + v_max * np.tanh(d_safe)

# Initial positions and velocities
x = np.linspace(0, N*5, N)  # Cars spaced 5 units apart
v = np.ones(N) * v_max      # All cars start at max velocity

# Introduce a small perturbation to one car to trigger phantom jam
v[N//2] *= 0.5

positions = [x.copy()]
velocities = [v.copy()]

for t in np.arange(0, T, dt):
    x_next = np.roll(x, -1)  # Position of car ahead
    delta_x = x_next - x
    # Periodic boundary conditions
    delta_x[-1] = (x[0] + N*5) - x[-1]
    # OVM update
    dv = a * (V(delta_x) - v)
    v += dv * dt
    x += v * dt
    positions.append(x.copy())
    velocities.append(v.copy())

positions = np.array(positions)
velocities = np.array(velocities)

# Create an animation of cars on a circular track and save as GIF
track_length = N * 5
theta = (positions % track_length) / track_length * 2 * np.pi
x_circle = np.cos(theta)
y_circle = np.sin(theta)

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')
scat = ax.scatter(x_circle[0], y_circle[0], s=50, c='C0')
# Optionally draw track
track = plt.Circle((0,0), 1.0, color='gray', fill=False, lw=1)
ax.add_patch(track)

def update(frame):
    scat.set_offsets(np.column_stack((x_circle[frame], y_circle[frame])))
    return (scat,)

fps = int(1/dt) if dt < 1 else 10
anim = animation.FuncAnimation(fig, update, frames=positions.shape[0], interval=1000/fps, blit=True)

# Save as GIF using PillowWriter (requires pillow). If not installed, instruct user to install it.
gif_path = 'ovm_simulation.gif'
try:
    writer = animation.PillowWriter(fps=fps)
    anim.save(gif_path, writer=writer)
    print(f'GIF saved to {gif_path}')
except Exception as e:
    print('Failed to save GIF:', e)
    print('If Pillow is missing, install it with: pip install pillow')
