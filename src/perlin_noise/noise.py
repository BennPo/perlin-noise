#from javarandom import Random
import numpy as np
import random
import matplotlib.pyplot as plt


class PerlinNoise():
    def __init__(self, seed, octaves):
        self.seed = seed
        self.octaves = octaves
        self.x = 0
        self.y = 0
        self.permutation = []
        for _ in range(2):
            for i in range(256):
                self.permutation.append(i)
        rng = random.Random(self.seed)
        rng.shuffle(self.permutation)

    def find_location(self, x, y):
        self.x = x - int(x)
        self.y = y - int(y)
        self.x_coord = int(x)
        self.y_coord = int(y)

    def distance(self):
        self.distance_to_tl =  (self.x, 1-self.y)
        self.distance_to_tr = (1-self.x, 1-self.y)
        self.distance_to_bl = (self.x, self.y)
        self.distance_to_br = (1-self.x, self.y)
    
    def dot_product(self):
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
        self.lerp_top = self.tl_dot + self.u * (self.tr_dot - self.tl_dot)
        self.lerp_bot = self.bl_dot + self.u * (self.br_dot - self.bl_dot)
        self.fin_lerp = self.lerp_bot + self.v * (self.lerp_top - self.lerp_bot)
        #print(self.fin_lerp)
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

        return total / max_amplitude


test1 = PerlinNoise(random.randint(0,1000000000), 2)

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