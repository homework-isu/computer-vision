import os

import matplotlib.pyplot as plt
import numpy as np


def calculate_resolution(filename):
    with open(filename, "r") as file:
        size = float(file.readline())
        img = np.loadtxt(file)

    obj = [row for row in img if 1 in row]
    width = len(obj)

    if width == 0:
        return 0

    return size / width


def show_fig(ax, filename, resolution, number):
    with open(filename, "r") as file:
        _ = file.readline()
        img = np.loadtxt(file)

    ax.imshow(img)
    ax.set_title(f"figure {number + 1}")
    ax.set_xlabel(f"resolution = {resolution} mm/px")


figuresDir = "figures"
figures = os.listdir(figuresDir)
resolutions = []
fig, axes = plt.subplots(2, 3, figsize=(8, 6), )

for figure in figures:
    resolutions += [round(calculate_resolution(figuresDir + '/' + figure), 3)]

for i, figure in enumerate(figures):
    j = int(i / 3)
    k = int(i % 3)
    show_fig(axes[j, k], f"{figuresDir}/{figure}", resolutions[i], i)

plt.subplots_adjust(wspace=1)
plt.show()
