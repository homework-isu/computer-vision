import numpy as np
from scipy.ndimage import binary_erosion, label


def find_by_pattern(img, pattern):
    _, c = label(binary_erosion(img, pattern))
    return c


p_pattern = np.array([[0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [1, 1, 1, 1, 1],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0]])

c_pattern = np.array([[1, 0, 0, 0, 1],
                     [0, 1, 0, 1, 0],
                     [0, 0, 1, 0, 0],
                     [0, 1, 0, 1, 0],
                     [1, 0, 0, 0, 1]])

data = np.load("stars.npy")

print(f"Count of stars: {find_by_pattern(data, p_pattern) + find_by_pattern(data, c_pattern)}")
