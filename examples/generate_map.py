import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from perlin_noise import generate_noise

# Generates nosie map
noise_map = generate_noise(130105, 4)

# shows 2D nosie map
plt.imshow(noise_map, cmap="gray")
plt.colorbar()
plt.show()


# it can be used as a hight map in 3d
x, y = np.meshgrid(range(noise_map.shape[0]), range(noise_map.shape[1]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, noise_map)
plt.title('z as 3d height map')
plt.show()