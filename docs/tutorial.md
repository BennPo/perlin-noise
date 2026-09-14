# Perlin Noise Tutorial

This tutorial shows how to generate and display Perlin noise using this package.
## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/BennPo/perlin-noise.git
```

## Import

```python
from perlin_noise import generate_noise
```

Basic usage
```python
noise_map = generate_noise(130105, 4)
```
This generates a noise map using:

```text
130105 as the seed
4 octaves
```

The default map size and scale are used unless you specify them.

## Custom size and scale

```python
noise_map = generate_noise(
    seed=130105,
    octaves=4,
    width=100,
    height=100,
    scale=0.05
)
```

Parameters:

* seed - controls the generated pattern
* octaves - controls how many layers of noise are combined
* width - width of the output map
* height - height of the output map
* scale - controls the size of the noise features

Smaller scale values produce larger, smoother features, while larger values produce smaller, more frequent features.

## Displaying the noise

```python
import matplotlib.pyplot as plt

plt.imshow(noise_map, cmap="gray")
plt.colorbar()
plt.show()
```

## Full example
```python
from perlin_noise import generate_noise
import matplotlib.pyplot as plt

noise_map = generate_noise(
    seed=130105,
    octaves=4,
    width=100,
    height=100,
    scale=0.05
)

plt.imshow(noise_map, cmap="gray")
plt.colorbar()
plt.show()
```