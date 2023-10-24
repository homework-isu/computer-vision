import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label

def extract_img(img, l):
    idxs = np.where(img == l)
    y_max, y_min = np.max(idxs[0]), np.min(idxs[0])
    x_max, x_min = np.max(idxs[1]), np.min(idxs[1])
    return img[y_min:y_max + 1, x_min:x_max + 1] // l

img = np.load("ps.npy.txt")
labeled_img, labels = label(img)

unique_figures = []
count_figures = []

for l in range(1, labels + 1):
    sub_img = extract_img(labeled_img, l)
    is_unique = True
    for i, u_fig in enumerate(unique_figures):
        if u_fig.shape == sub_img.shape and np.equal(u_fig, sub_img).all():
            count_figures[i] += 1
            is_unique = False
            break
    if is_unique:
        unique_figures.append(sub_img)
        count_figures.append(1)


num_unique_figures = len(unique_figures)
for i, (fig, count) in enumerate(zip(unique_figures, count_figures), start=1):
    plt.subplot(3, num_unique_figures // 2, i)
    if fig.size > 0:
        plt.imshow(fig, cmap='YlGn', vmin=0, vmax=1)
        plt.title(f'Фигура {i}\nКоличество: {count}')
    else:
        plt.axis('off')

plt.tight_layout()
plt.show()
