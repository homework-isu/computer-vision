import cv2
import numpy as np
import matplotlib.pyplot as plt
from circle import Circle


def get_circles(img):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circles = [c for c in contours if len(cv2.approxPolyDP(c, 0.04 * cv2.arcLength(c, True), True)) >= 6]

    coords = []
    for circle in circles:
        moments = cv2.moments(circle)
        center_x = int(moments["m10"] / moments["m00"])
        center_y = int(moments["m01"] / moments["m00"])

        coords += [(center_x, center_y)]
    return coords


def add_coords_to_circle(circle, coords, idx):
    circle.add_coords(coords[idx])
    coords.pop(idx)


files = [f'out/h_{i}.npy' for i in range(100)]
img0 = np.load(files[0])
circles_coords = get_circles(img0)

files = files[1:]

circle_1: Circle
circle_2: Circle
circle_3: Circle

circle_1 = Circle(circles_coords[0])
circle_2 = Circle(circles_coords[1])
circle_3 = Circle(circles_coords[2])

for file in files:
    img = np.load(file)
    coords = get_circles(img)
    idx = 0
    threshold = 5
    while len(coords) != 0:
        idx = (idx + 1) % len(coords)
        threshold += 5

        if circle_1.is_right_center(coords[idx], threshold):
            add_coords_to_circle(circle_1, coords, idx)
        elif circle_2.is_right_center(coords[idx], threshold):
            add_coords_to_circle(circle_2, coords, idx)
        elif circle_3.is_right_center(coords[idx], threshold):
            add_coords_to_circle(circle_3, coords, idx)

x_1, y_1 = circle_1.get_x(), circle_1.get_y()
x_2, y_2 = circle_2.get_x(), circle_2.get_y()
x_3, y_3 = circle_3.get_x(), circle_3.get_y()

plt.plot(x_1, y_1, label='circle 1')
plt.plot(x_2, y_2, label='circle 2')
plt.plot(x_3, y_3, label='circle 3')

plt.xlabel('X')
plt.ylabel('Y')
plt.legend()

plt.show()
