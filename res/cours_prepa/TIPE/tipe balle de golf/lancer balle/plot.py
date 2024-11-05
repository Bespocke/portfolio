#%% 
    
import matplotlib.pyplot as plt
import numpy as np

m = 1
g = 9.81

wx0, wy0, wz0 = 0, 0, 314
alpha = 0.01  

x, y, z = 0, 0, 0
vx, vy, vz = 100, 100, 1

dt = 0.0001
num_iterations = 10000

X, Y, Z = [x], [y], [z]

for _ in range(num_iterations):
    wx = wx0 * np.exp(-alpha * _)
    wy = wy0 * np.exp(-alpha * _)
    wz = wz0 * np.exp(-alpha * _)
    
    ax = 1/m * (0.25 * 1.2 * np.pi * vx * wx - 0.5 * 0.47 * 1.2 * np.pi * (vx**2))
    ay = 1/m * (0.25 * 1.2 * np.pi * vy * wy - 0.5 * 0.47 * 1.2 * np.pi * (vy**2))
    az = 1/m * (0.25 * 1.2 * np.pi * vz * wz - 0.5 * 0.47 * 1.2 * np.pi * (vz**2) - m * g)
    
    vx += ax * dt
    vy += ay * dt
    vz += az * dt

    x += vx 
    y += vy 
    z += vz 
    
    X.append(x)
    Y.append(y)
    Z.append(max(z, 0))

    if z <= 0:
        break

print("position en x :", X[-1])
print("position en y :", Y[-1])
print("position en z :", Z[-1])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(X, Y, Z)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

# %%
