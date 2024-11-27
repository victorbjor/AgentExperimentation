import numpy as np
from torch import Tensor


def polynomial_function(x, y):
    return 3*x**2 + 2*y + x*y - 5


def trig_function(x, y):
    return np.sin(x) + np.cos(y) + 0.5*np.sin(x*y)


def exponential_function(x, y):
    return np.exp(-x**2 - y**2) + 0.1*x*y


def radial_function(x, y):
    return np.sqrt(x**2 + y**2)


def gaussian_radial_function(x, y):
    return np.exp(-(x**2 + y**2) / 2.0)


def binary_decision(x, y):
    return 1 if x**2 + y**2 < 1 else 0


def checkerboard_function(x, y):
    return (int(x * 5) % 2) ^ (int(y * 5) % 2)  # XOR pattern
