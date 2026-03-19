"""
Duffing Oscillator Simulation using RK4

Includes:
- Time series
- Phase space
- Poincare section
- Resonance analysis
- Bifurcation diagram


Author: Saipayan Sanyal
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------- PARAMETERS ----------------
delta = 0.2
alpha = -1.0
beta  = 1.0
gamma = 0.3
omega = 1.2

# ---------------- TIME ----------------
dt = 0.01
t_max = 200
t = np.arange(0, t_max, dt)

# ---------------- ACCELERATION FUNCTION ----------------
def acceleration(x, v, t, gamma_val, omega_val):
    return -delta*v - alpha*x - beta*x**3 + gamma_val*np.cos(omega_val*t)

# ---------------- RK4 SOLVER ----------------
def rk4_solver(gamma_val=gamma, omega_val=omega):
    x = np.zeros(len(t))
    v = np.zeros(len(t))

    x[0] = 0.1
    v[0] = 0.0

    for i in range(len(t)-1):

        k1x = v[i]
        k1v = acceleration(x[i], v[i], t[i], gamma_val, omega_val)

        k2x = v[i] + 0.5*k1v*dt
        k2v = acceleration(x[i] + 0.5*k1x*dt,
                           v[i] + 0.5*k1v*dt,
                           t[i] + 0.5*dt,
                           gamma_val, omega_val)

        k3x = v[i] + 0.5*k2v*dt
        k3v = acceleration(x[i] + 0.5*k2x*dt,
                           v[i] + 0.5*k2v*dt,
                           t[i] + 0.5*dt,
                           gamma_val, omega_val)

        k4x = v[i] + k3v*dt
        k4v = acceleration(x[i] + k3x*dt,
                           v[i] + k3v*dt,
                           t[i] + dt,
                           gamma_val, omega_val)

        x[i+1] = x[i] + (dt/6)*(k1x + 2*k2x + 2*k3x + k4x)
        v[i+1] = v[i] + (dt/6)*(k1v + 2*k2v + 2*k3v + k4v)

    return x, v

# ---------------- MAIN SIMULATION ----------------
x, v = rk4_solver()

# ---------------- TIME SERIES ----------------
plt.figure()
plt.plot(t, x)
plt.xlabel("Time")
plt.ylabel("x(t)")
plt.title("Time Series")
plt.grid()
plt.show()

# ---------------- PHASE SPACE ----------------
plt.figure()
plt.plot(x, v)
plt.xlabel("x")
plt.ylabel("v")
plt.title("Phase Space")
plt.grid()
plt.show()

# ---------------- POINCARE SECTION ----------------
T = 2*np.pi / omega
indices = (t % T) < dt

plt.figure()
plt.scatter(x[indices], v[indices], s=2)
plt.xlabel("x")
plt.ylabel("v")
plt.title("Poincare Section")
plt.grid()
plt.show()

# ---------------- RESONANCE ANALYSIS ----------------
omegas = np.linspace(0.5, 2.0, 50)
amplitudes = []

for w in omegas:
    x_temp, _ = rk4_solver(gamma, w)
    amp = np.max(np.abs(x_temp[-2000:]))
    amplitudes.append(amp)

plt.figure()
plt.plot(omegas, amplitudes)
plt.xlabel("Driving Frequency (omega)")
plt.ylabel("Amplitude")
plt.title("Resonance Curve")
plt.grid()
plt.show()

# ---------------- BIFURCATION DIAGRAM ----------------
gammas = np.linspace(0.2, 0.6, 80)
x_vals = []

for g in gammas:
    x_temp, _ = rk4_solver(g, omega)
    x_vals.extend(x_temp[-1000:])

plt.figure()
plt.scatter(np.repeat(gammas, 1000), x_vals, s=1)
plt.xlabel("Gamma")
plt.ylabel("x")
plt.title("Bifurcation Diagram")
plt.show()

