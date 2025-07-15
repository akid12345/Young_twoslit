import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Setup
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(-2, 14)
ax.set_ylim(-4, 4)
ax.axis('off')

# Static elements
ax.plot(-1.5, 0, 'yo', markersize=12)
ax.text(-1.8, 0.5, 'Source A', fontsize=10)

# Barrier with slits
ax.plot([2, 2], [-3.5, 3.5], color='blue', linewidth=4)
slit_y = [1, -1]
for y in slit_y:
    ax.plot(2, y, 'white', markersize=12, marker='s')
    ax.text(2.2, y + 0.3, f'S{1 if y > 0 else 2}', fontsize=10)

# Screen
ax.plot([12, 12], [-3.5, 3.5], color='blue', linewidth=4)

# Wavefront storage
source_wavefronts = []
slit_wavefronts = [[], []]  # For S1 and S2

# Create initial empty wavefronts
def create_wavefront():
    return ax.plot([], [], 'red', alpha=0.3)[0]

def create_source_wavefront():
    return ax.plot([], [], 'orange', alpha=0.5)[0]

# Animation function
def animate(frame):
    # Emit new wavefronts more frequently
    if frame % 5 == 0:
        source_wavefronts.append({'radius': 0.5, 'line': create_source_wavefront()})
        for j in range(2):
            slit_wavefronts[j].append({'radius': 0.5, 'line': create_wavefront()})

    # Update source wavefronts
    for wf in source_wavefronts:
        wf['radius'] += 0.1  # Smaller increment for denser waves
        r = wf['radius']
        theta = np.linspace(-np.pi/2, np.pi/2, 400)  # More points for smoother curves
        x = r * np.cos(theta) - 1.5
        y = r * np.sin(theta)
        x = np.clip(x, -2, 2)
        wf['line'].set_data(x, y)

    # Update slit wavefronts
    for j, y0 in enumerate(slit_y):
        for wf in slit_wavefronts[j]:
            wf['radius'] += 0.1
            r = wf['radius']
            theta = np.linspace(-np.pi/2, np.pi/2, 400)
            x = r * np.cos(theta) + 2
            y = r * np.sin(theta) + y0
            x = np.clip(x, 2, 12)
            wf['line'].set_data(x, y)

    return [wf['line'] for wf in source_wavefronts] + \
           [wf['line'] for group in slit_wavefronts for wf in group]

# Run animation
ani = FuncAnimation(fig, animate, frames=300, interval=50, blit=True)
plt.show()
