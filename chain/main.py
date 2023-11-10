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
        if (0 <= neighbor_x < img.shape[1] and
            0 <= neighbor_y < img.shape[0] and
            img[neighbor_y, neighbor_x] == 0) or \
           (neighbor_x == img.shape[1] or neighbor_y == img.shape[0]):
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


def are_equal_chains(ch1, ch2):
    ch1_copy = ch1.copy()
    n = len(ch1_copy)

    while ch1_copy != ch2 and n > 0:
        ch1_copy = [ch1_copy[i - 1] for i in range(len(ch1_copy))]
        n -= 1
    return ch1_copy == ch2


data1 = np.array(
    [
        [0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0],
    ]
)

data2 = np.array(
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

print(data1.shape)
dirs1, perimeter1 = chain(data1, 1)
dirs2, perimeter2 = chain(data2, 1)
print("perimeter points of data 1:", perimeter1)
print("nums of dirs of data 1:", dirs1)

print("perimeter points of data 2:", perimeter2)
print("nums of dirs of data 2:", dirs2)

print(are_equal_chains(dirs1, dirs2))

plt.subplots(nrows=1, ncols=2)
plt.subplot(1, 2, 1)
plt.imshow(data1)
plt.scatter([point[1] for point in perimeter1], [point[0] for point in perimeter1], c='r')

plt.subplot(1, 2, 2)
plt.imshow(data2)
plt.scatter([point[1] for point in perimeter2], [point[0] for point in perimeter2], c='r')
plt.show()
