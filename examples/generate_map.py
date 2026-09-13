import numpy as np
import matplotlib.pyplot as plt

from perlin_noise import PerlinNoise

test1 = PerlinNoise(1, 8)

noise_map = []

for y in range(100):
    row = []

    for x in range(100):
        x_val = x * 0.05
        y_val = y * 0.05
        test1.find_location(x_val, y_val)
        test1.get_gradients()
        test1.distance()
        test1.dot_product()
        test1.fade()
        result = test1.lerp()
        row.append(result)

    noise_map.append(row)


noise_map = np.array(noise_map)

plt.imshow(noise_map, cmap="gray")
plt.colorbar()
plt.show()