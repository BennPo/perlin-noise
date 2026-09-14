import numpy as np
import random
import matplotlib.pyplot as plt


class PerlinNoise():
    def __init__(self, seed, octaves):
        self.seed = seed
        self.octaves = octaves
        self.x = 0
        self.y = 0

        # Create and shuffle the permutation table using the seed
        self.permutation = []
        for _ in range(2):
            for i in range(256):
                self.permutation.append(i)
        rng = random.Random(self.seed)
        rng.shuffle(self.permutation)

    def find_location(self, x, y):
        # Find the current lattice cell and the point's local position inside it
        self.x = x - int(x)
        self.y = y - int(y)
        self.x_coord = int(x)
        self.y_coord = int(y)

    def distance(self):
        # Calculate displacement vectors from each corner to the sample point
        self.distance_to_tl =  (-self.x, 1-self.y)
        self.distance_to_tr = (1-self.x, 1-self.y)
        self.distance_to_bl = (-self.x, -self.y)
        self.distance_to_br = (1-self.x, -self.y)
    
    def dot_product(self):
        # Calculate the contribution from each corner using dot products
        self.tl_dot = np.dot(self.vec_tl, self.distance_to_tl)
        self.tr_dot = np.dot(self.vec_tr, self.distance_to_tr)
        self.bl_dot = np.dot(self.vec_bl, self.distance_to_bl)
        self.br_dot = np.dot(self.vec_br, self.distance_to_br)

    def get_gradients(self):
        self.gradients = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),

            (0.707, 0.707),
            (-0.707, 0.707),
            (0.707, -0.707),
            (-0.707, -0.707)
        ]

        # Select one gradient vector for each corner of the cell
        self.value_tl = self.permutation[self.permutation[self.x_coord] + self.y_coord+1]
        self.value_tr = self.permutation[self.permutation[self.x_coord+1] + (self.y_coord+1)]
        self.value_bl = self.permutation[self.permutation[self.x_coord] + (self.y_coord)]
        self.value_br = self.permutation[self.permutation[self.x_coord+1] + (self.y_coord)]

        self.vec_tl = self.gradients[self.value_tl % 8]
        self.vec_tr = self.gradients[self.value_tr % 8]
        self.vec_bl = self.gradients[self.value_bl % 8]
        self.vec_br = self.gradients[self.value_br % 8]

    def fade(self):
        self.u = 6*self.x **5 -15*self.x**4 +10*self.x**3
        self.v = 6*self.y **5 -15*self.y**4 +10*self.y**3

    def lerp(self):
        # Interpolate horizontally, then vertically, to get the final noise value
        self.lerp_top = self.tl_dot + self.u * (self.tr_dot - self.tl_dot)
        self.lerp_bot = self.bl_dot + self.u * (self.br_dot - self.bl_dot)
        self.fin_lerp = self.lerp_bot + self.v * (self.lerp_top - self.lerp_bot)
        return self.fin_lerp

    def noise(self, x, y):
        self.find_location(x, y)
        self.get_gradients()
        self.distance()
        self.dot_product()
        self.fade()
        result = self.lerp()
        return result

    def octave_noise(self, x, y):
        # Combine multiple octaves at increasing frequency and decreasing amplitude
        total = 0
        frequency = 1
        amplitude = 1
        max_amplitude = 0

        for _ in range(self.octaves):
            total += self.noise(
                x * frequency,
                y * frequency
            ) * amplitude

            max_amplitude += amplitude

            frequency *= 2
            amplitude *= 0.5

        # Normalise the combined octave value
        return total / max_amplitude



# main function to get the noise map
def generate_noise(seed, octaves, width=100, height=100, scale=0.05):
    perlin = PerlinNoise(seed, octaves)

    noise_map = []

    # Sample the noise function across a 2D grid
    for y in range(height):
        row = []

        for x in range(width):
            x_val = x * scale
            y_val = y * scale
            result = perlin.octave_noise(x_val, y_val)
            row.append(result)

        noise_map.append(row)

    # Return the completed map as a NumPy array
    return np.array(noise_map)