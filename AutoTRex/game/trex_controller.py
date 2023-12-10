import time
import cv2
import keyboard
import matplotlib.pyplot as plt
import numpy as np
from .screen_controller import ScreenController


class TrexController:
    def __init__(self):
        self.finder = ScreenController()
        self.start_time = time.time()
        self.is_game_step = False
        self.crouch_delay = 0.3

    def start_game(self):
        self.finder.process_screenshot()
        self.is_game_step = True

    def stop_game(self):
        self.is_game_step = False

    def find_offset(self):
        current_time = time.time()
        score = (current_time - self.start_time) * 10

        if score < 1000:
            offset = int((score // 100) * 7)
        else:
            offset = int(min((score // 100) * 15, 190))

        return offset

    def process_game(self, offset):
        if self.is_game_step:
            bottom_obstacles_image = self.finder.find_bottom_obstacle(horizontal_offset=offset)
            if np.any(bottom_obstacles_image < 150):
                self.jump()

    def jump(self):
        keyboard.release('down')
        keyboard.press('space')
        time.sleep(self.crouch_delay)
        keyboard.release('space')
        keyboard.press('down')
        time.sleep(0.15)

    def play_game_step(self):
        offset = self.find_offset()
        self.process_game(offset)
