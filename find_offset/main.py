import numpy as np
import matplotlib.pyplot as plt


def load_img(filename):
    with open(filename) as file:
        _ = file.readline()
        img = np.loadtxt(file)
    return img


def find_offset(img1, img2):
    corr = np.correlate(img1.ravel(), img2.ravel(), mode='full')

    y, x = divmod(np.argmax(corr), img2.shape[1])
    return y - img1.shape[0] + 1, x - img1.shape[1] + 1


image1 = load_img("img/img1.txt")
image2 = load_img("img/img2.txt")

offset = find_offset(image1, image2)
print(f"offset is (y, x): {offset}")