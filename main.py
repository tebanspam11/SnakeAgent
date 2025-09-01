from config import *
from Environment import Environment

import time

if __name__ == "__main__":
    environment = Environment(ROWS, COLUMNS, TILE_SIZE, TOP, LEFT, MOVE_INTERVAL)

    print("You have 3 seconds to switch to the game window...")
    time.sleep(3)

    environment.play()