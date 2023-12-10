import cv2
import numpy as np
from mss import mss

IMG_WIDTH = 100
IMG_HEIGHT = 200

class ScreenController:
    def __init__(self, dino_path='files/trex.png'):
        self.capturer = mss()
        self.monitor = self.capturer.monitors[0]

        self.trex_img = cv2.imread(dino_path, cv2.IMREAD_GRAYSCALE)
        self.trex_img = cv2.Canny(self.trex_img, IMG_WIDTH, IMG_HEIGHT)

        self.trex_position = None

        self.trex_size = [0, 0]

    def find_bottom_obstacle(self, horizontal_offset):
        params = {
            "top": self.trex_position[1] + 5,
            "left": self.trex_position[0] + self.trex_size[0],
            "width": self.trex_size[0] + horizontal_offset,
            "height": 25
        }

        screenshot = np.array(self.capturer.grab(params))
        return screenshot

    def find_trex(self, screenshot):
        w, h = self.trex_img.shape
        result = cv2.matchTemplate(screenshot, self.trex_img, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        return max_loc, (w, h)

    def update_trex_position(self, trex_position, trex_size):
        self.trex_position = trex_position
        self.trex_size[0], self.trex_size[1] = trex_size

    def process_screenshot(self):
        screenshot = self.capturer.grab(self.monitor)
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        screenshot = cv2.Canny(screenshot, IMG_WIDTH, IMG_HEIGHT)
        position, size = self.find_trex(screenshot)

        self.update_trex_position(position, size)
        return self.trex_position, (self.trex_position[0] + self.trex_size[0],
                                    self.trex_position[1] + self.trex_size[1])
