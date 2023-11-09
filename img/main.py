import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def filling_factor(region):
    return region.image.mean()

def recognize(reqion):
    if filling_factor(reqion) == 1:
        return "-"
    else:
        euler = region.euler_number
        match euler:
            case 1:
                pass
            case 0:
                pass
            case -1:
                if 1 in region.image.mean(0):
                    return "B"
                else:
                    return "8"
    return "?"

img = plt.imread("alphabet.png")
binary = img.mean(2)
binary[binary > 0] = 1
labaled = label(binary)
print(labaled.max())
regions = regionprops(labaled)

counts = {}
for region in regions:
    symbol = recognize(region)
    if symbol not in counts:
        counts[symbol] = 1
        plt.imshow(region.image)
        plt.show()
    else:
        counts[symbol] += 1

print(regions[7].euler_number)
print(regions[1].euler_number)

print(counts)