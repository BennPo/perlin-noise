import numpy as np
import random
import matplotlib.pyplot as plt

from perlin_noise import PerlinNoise

test1 = PerlinNoise(random.randint(0,1000000000), 4)

noise_map = []

for y in range(100):
    row = []

    for x in range(100):
        x_val = x * 0.05
        y_val = y * 0.05
        result = test1.octave_noise(x_val, y_val)
        row.append(result)

    noise_map.append(row)


noise_map = np.array(noise_map)

plt.imshow(noise_map, cmap="gray")
plt.colorbar()
plt.show()