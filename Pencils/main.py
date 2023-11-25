import os

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters, measure


def is_pencil(region):
    return region.perimeter > 2500 and 30 > (region.major_axis_length / region.minor_axis_length) > 15


def make_binary_img(img):
    thresh = filters.threshold_otsu(img)
    return img < thresh


def count_pencils_from_image(img_path, show=False):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    binary_img = make_binary_img(img)

    _, label = cv2.connectedComponents(binary_img.astype(np.uint8))

    pencils_count = 0
    for region in measure.regionprops(label):
        if is_pencil(region):
            plt.imshow(region.image)
            pencils_count += 1

    if show:
        draw_pencils_plot(binary_img, label, pencils_count, img_path.split("/")[-1])

    return pencils_count


def draw_pencils_plot(img, label, pencils_count, img_filename):
    pencils_contour = np.zeros_like(img)

    for region in measure.regionprops(label):
        if is_pencil(region):
            pencils_contour[region.coords[:, 0], region.coords[:, 1]] = 255

    plt.imshow(img, cmap='gray')
    plt.contour(pencils_contour, colors='green', linewidths=2)
    plt.title(f'{img_filename}\npencils count: {pencils_count}')
    plt.show()


directory = "files/"
show = False

imgs_dir = os.listdir(directory)
pencils_count = 0
for img_file in imgs_dir:
    pencils_count += count_pencils_from_image(directory + "/" + img_file, show)

print("Pencils count:", pencils_count)

