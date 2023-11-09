import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def filling_factor(region):
    return region.image.mean()


def recognize(region):
    if filling_factor(region) == 1:
        return "-"
    else:
        euler = region.euler_number
        match euler:
            case 1:
                if region.image[-1, 0] == 1 and region.image[0, -1] == 1:
                    if region.image[-1, -1] == 1 and region.image[0, 0] == 1:
                        return "X"
                    else:
                        return "/"
                elif 1 in region.image.mean(0):
                    return "1"
                elif region.image[0, 0] == 1 and region.image[0, -1] == 1:
                    return "W"

                pass
            case 0:
                if 1 in region.image.mean(0) and region.image[0, 0] == 1 and region.image[-1, 0] == 1:
                    if region.image[region.image.shape[0] // 2, region.image.shape[1] // 2] == 1:
                        return "P"
                    else:
                        return "D"
                if region.image[-1, 0] == 1:
                    return "A"
                elif region.image[region.image.shape[0] // 2, region.image.shape[1] // 2] == 0:
                    return "0"
            case -1:
                if 1 in region.image.mean(0):
                    return "B"
                else:
                    return "8"
    return "*"


def count_symbols(binary, show=False):
    labeled = label(binary)

    regions = regionprops(labeled)

    counts = {}
    n = 0
    for region in regions:
        symbol = recognize(region)
        n += 1
        if symbol not in counts:
            counts[symbol] = 1
            if show:
                plt.imshow(region.image, vmin=0, vmax=1)
                plt.xlabel(symbol)
                plt.show()
        else:
            counts[symbol] += 1
    return counts, n


def get_binary(filename):
    img = plt.imread(filename)
    binary = img.mean(2)

    binary[binary == 1] = 0
    binary[binary != 0] = 1

    return binary


if __name__ == '__main__':
    img = get_binary("alphabet.png")
    symbols, n = count_symbols(img, False) # show=True чтобы посмотреть, как распознаются символы
    for symbol in symbols:
        print(f"{symbol} - {round((symbols[symbol] / n), 2)}%")