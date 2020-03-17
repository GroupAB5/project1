import matplotlib.pyplot as plt
import numpy as np

R_e = 6371e3 # earth radius in meters

ALGO_STA_X = 0.918129456521166E+06/R_e
ALGO_STA_Y = -0.434607124320611E+07/R_e
ALGO_STA_Z = 0.456197783555769E+07/R_e

#ALGO_STA_X, ALGO_STA_Y, ALGO_STA_Z = getCoord("dps_data/PZITRF08001.00X")[0]/R_e

# +-  0.110641654490017E-02
# +-  0.202139649818358E-02
# +-  0.197912368098458E-02

# Make data
u = np.linspace(0, 2 * np.pi, 100)  # polar angle theta [0,2pi]
v = np.linspace(0, np.pi, 100)      # polar angle phi [0,pi]
x = np.outer(np.cos(u)*np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

# Plot the surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_wireframe(x, y, z, color='b', rcount = 20, ccount = 20)
ax.scatter(ALGO_STA_X,ALGO_STA_Y,ALGO_STA_Z, color = "red")
ax.set_xlabel("x axis [earth radius]")
plt.show()