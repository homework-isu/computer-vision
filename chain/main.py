import numpy as np
import matplotlib.pyplot as plt


def get_num(y, x):
    match (y, x):
        case (0, 1):
            return 0
        case (1, 1):
            return 1
        case (1, 0):
            return 2
        case (1, -1):
            return 3
        case (0, -1):
            return 4
        case (-1, -1):
            return 5
        case (-1, 0):
            return 6
        case (-1, 1):
            return 7


def is_perimeter_point(y, x, img):
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dy, dx in dirs:
        neighbor_y, neighbor_x = y + dy, x + dx
        if 0 <= neighbor_x < img.shape[1] and 0 <= neighbor_y < img.shape[0] and img[neighbor_y, neighbor_x] == 0:
            return True

    return False


def neighbors(y, x, img, perimeter):
    dirs = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    for dy, dx in dirs:
        n_y, n_x = y + dy, x + dx
        if 0 <= n_y < img.shape[0] and 0 <= n_x < img.shape[1] and img[n_y, n_x] == 1 and (n_y, n_x) not in perimeter and is_perimeter_point(n_y, n_x, img):
            num_of_dir = get_num(dy, dx)
            return n_y, n_x, num_of_dir

    return None, None, None


def chain(img, label=1):
    y_start, x_start = None, None

    for y in range(img.shape[1]):
        for x in range(img.shape[0]):
            if img[y, x] == label:
                y_start, x_start = y, x
                break
        if not y_start is None:
            break

    if y_start is None or x_start is None:
        return []

    perimeter = []
    dirs = []

    while True:
        if (y, x) not in perimeter:
            perimeter += [(y, x)]

        y, x, num_dirs = neighbors(y, x, img, perimeter)
        if num_dirs is not None:
            dirs += [num_dirs]

        if (len(perimeter) == 0 and (y, x) == (y_start, x_start)) or y is None or x is None:
            break

    return dirs, perimeter


data = np.array(
    [
        [0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
    ]
)

dirs, perimeter = chain(data, 1)
print("perimeter points:", perimeter)
print("nums of dirs:", dirs)

plt.imshow(data)
plt.scatter([point[1] for point in perimeter], [point[0] for point in perimeter], c='r')
plt.show()
