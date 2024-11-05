#%%

import matplotlib.pyplot as plt
import numpy as np

m = 0.045  
g = 9.81  

wx0, wy0, wz0 = 0, 100, 0
alpha = 0.01  

x, y, z = 0, 0, 0  

v0 = 70 

vx = v0 
vy = v0 
vz = 1

dt = 0.000001  
num_iterations = 10000000

X, Y, Z = [], [], []

def update_state(x, y, z, vx, vy, vz, dt, i):

    ax = 1/m * (0.25 * 1.2 * np.pi * vx * wx0 - 0.5 * 0.47 * 1.2 * np.pi * (vx**2))
    ay = 1/m * (0.25 * 1.2 * np.pi * vy * wy0 - 0.5 * 0.47 * 1.2 * np.pi * (vy**2))
    az = 1/m * (0.25 * 1.2 * np.pi * vz * wz0 - 0.5 * 0.47 * 1.2 * np.pi * (vz**2) - m * g)

    k1x = vx * dt
    k1y = vy * dt
    k1z = vz * dt
    k1vx = ax * dt
    k1vy = ay * dt
    k1vz = az * dt

    k2x = (vx + 0.5 * k1vx) * dt
    k2y = (vy + 0.5 * k1vy) * dt
    k2z = (vz + 0.5 * k1vz) * dt
    k2vx = ax * dt
    k2vy = ay * dt
    k2vz = az * dt

    k3x = (vx + 0.5 * k2vx) * dt
    k3y = (vy + 0.5 * k2vy) * dt
    k3z = (vz + 0.5 * k2vz) * dt
    k3vx = ax * dt
    k3vy = ay * dt
    k3vz = az * dt

    k4x = (vx + k3vx) * dt
    k4y = (vy + k3vy) * dt
    k4z = (vz + k3vz) * dt
    k4vx = ax * dt
    k4vy = ay * dt
    k4vz = az * dt

    new_x = x + (k1x + 2 * k2x + 2 * k3x + k4x) / 6
    new_y = y + (k1y + 2 * k2y + 2 * k3y + k4y) / 6
    new_z = max(z + (k1z + 2 * k2z + 2 * k3z + k4z) / 6, 0)
    new_vx = vx + (k1vx + 2 * k2vx + 2 * k3vx + k4vx) / 6
    new_vy = vy + (k1vy + 2 * k2vy + 2 * k3vy + k4vy) / 6
    new_vz = vz + (k1vz + 2 * k2vz + 2 * k3vz + k4vz) / 6

    return new_x, new_y, new_z, new_vx, new_vy, new_vz

for i in range(1, num_iterations + 1):
    x, y, z, vx, vy, vz = update_state(x, y, z, vx, vy, vz, dt, i)

    if z <= 0:
        break

    X.append(x*1000)
    Y.append(y*1000)
    Z.append(z*1000)

print("position en x :", X[-1])
print("position en y :", Y[-1])
print("position en z :", Z[-1])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(X, Y, Z)

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')

plt.show()


# %%

