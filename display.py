import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# === Simulation Settings ===
width = 800                # Screen resolution (pixels)
num_photons = 10000        # Total number of photons
slit_distance = 0.1        # Distance between slits (meters)
wavelength = 0.005         # Wavelength of light (meters)
screen_distance = 1.0      # Distance from slits to screen (meters)
screen_width = 0.5         # Physical width of the screen (meters)

# === Derived Values ===
x = np.linspace(-screen_width/2, screen_width/2, width)
k = 2 * np.pi / wavelength
intensity = np.zeros(width)

# === Interference Pattern Calculation ===
def wave_intensity(x):
    theta1 = np.arctan2(x + slit_distance/2, screen_distance)
    theta2 = np.arctan2(x - slit_distance/2, screen_distance)

    phase1 = k * slit_distance/2 * np.sin(theta1)
    phase2 = -k * slit_distance/2 * np.sin(theta2)

    # Interference from two slits (superposition of two waves)
    E = np.cos(phase1) + np.cos(phase2)
    return E**2  # Intensity is square of electric field

# === Normalize Probability Distribution ===
prob_dist = wave_intensity(x)
prob_dist /= np.sum(prob_dist)  # Normalize to make it a probability distribution

# === Photon Hit Distribution ===
hits = np.random.choice(np.arange(width), size=num_photons, p=prob_dist)

# === Histogram for animation ===
hist = np.zeros(width)

# === Plot Setup ===
fig, ax = plt.subplots()
line, = ax.plot(x, hist, color='blue')
ax.set_ylim(0, max(prob_dist)*num_photons/50)
ax.set_xlim(-screen_width/2, screen_width/2)
ax.set_title("Screen Displaying Interference Pattern")
ax.set_xlabel("Screen Position")
ax.set_ylabel("Photon Count")

# === Animation Function ===
def animate(i):
    global hist
    if i < len(hits):
        hist[hits[i]] += 1
    if i % 10 == 0:  # Update less frequently for speed
        line.set_ydata(hist)
    return [line]

ani = animation.FuncAnimation(fig, animate, frames=num_photons, interval=1, blit=True)
plt.show()

