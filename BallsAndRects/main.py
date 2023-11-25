import numpy as np
from matplotlib import pyplot as plt
from skimage.measure import label
# from scipy.ndimage import label
import cv2

img = cv2.imread("balls_and_rects.png")
hues = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

th, img_gray_thresh_otsu = cv2.threshold(hues, 128, 192, cv2.THRESH_OTSU)
labeled = label(img_gray_thresh_otsu)

results = {}

circles = 0
rects = 0

for i in range(1, np.max(labeled) + 1):
    figure = np.where(labeled == i)

    y_min, x_min = figure[0][0], figure[1][0]
    y_max, x_max = figure[0][-1], figure[1][-1]

    hue = img[y_min][x_min][0]
    if hue not in results:
        results[hue] = {"rects": 0, "circles": 0}

    if (x_max - x_min + 1) * (y_max - y_min + 1) == len(figure[0]):
        results[hue]["rects"] += 1
        rects += 1
    else:
        results[hue]["circles"] += 1
        circles += 1

print(f"Hues count: {len(results)}")
print(f"Figures count: {np.max(labeled)}")

print(f"Rects: {rects}")
print(f"Circles: {circles}")

for hue in results:
    print(f"Hue - {hue}: rects: {results[hue]['rects']}, circles: {results[hue]['circles']}")
