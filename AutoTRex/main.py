import time

from game import TrexController
import keyboard

game_controller = TrexController()
print("Press 'Space' to start the game")
while True:
    if keyboard.is_pressed('space'):
        print("Game started")
        time.sleep(1)
        game_controller.start_game()

    if keyboard.is_pressed('esc'):
        print("Game stopped")
        time.sleep(1)
        game_controller.stop_game()

    if game_controller.is_game_step:
        game_controller.play_game_step()
