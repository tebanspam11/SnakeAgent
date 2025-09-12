import random

from Snake import Snake
from Agent import Agent
from config import *

directionMap = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
pathMap = {(1, 0): "down", (0, 1): "right", (-1, 0): "up", (0, -1): "left"}

class Game:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.snake = Snake()
        self.apple = self.spawnApple()
        self.score = 0
        self.steps = 0

    def spawnApple(self):
        """Generate a new apple in a free cell."""

        free_cells = [
            (i, j) for i in range(self.rows) for j in range(self.cols)
            if (i, j) not in self.snake.getBody()
        ]
        return random.choice(free_cells) if free_cells else None

    def step(self, direction):
        """Perform one move of the snake in the given direction."""

        head = self.snake.getHead()
        dx, dy = directionMap[direction]
        newHead = (head[0] + dx, head[1] + dy)

        # check collisions
        if (newHead[0] < 0 or newHead[0] >= self.rows or
            newHead[1] < 0 or newHead[1] >= self.cols or
            newHead in self.snake.getBody()):
            return False

        # check apple eating or normal move
        if newHead == self.apple:
            self.snake.move(newHead, grow=True)
            self.apple = self.spawnApple()
            self.score += 1
        else:
            self.snake.move(newHead, grow=False)

        self.steps += 1
        return True


def simulate_once(rows, cols, agent):
    """Simulate a single game and return statistics (score, steps, time)."""

    game = Game(rows, cols)

    while True:
        path = agent.compute(game.apple, game.snake)
        if not path:  # no path available
            break

        for direction in path:
            alive = game.step(direction)
            if not alive:
                return game.score, game.steps, game.steps * MOVE_INTERVAL

    return game.score, game.steps, game.steps * MOVE_INTERVAL


def simulate_n_games(n, rows=ROWS, cols=COLUMNS):
    """Run n simulations and return averages."""

    agent = Agent(rows, cols)

    total_score = 0
    total_steps = 0
    total_time = 0.0

    for _ in range(n):
        score, steps, time_survived = simulate_once(rows, cols, agent)
        total_score += score
        total_steps += steps
        total_time += time_survived

    avg_score = total_score / n
    avg_steps = total_steps / n
    avg_time = total_time / n

    print(f"\nAfter {n} games:")
    print(f"  Average score: {avg_score:.2f}")
    print(f"  Average steps: {avg_steps:.2f}")
    print(f"  Average time: {avg_time:.2f} s")

    return avg_score, avg_steps, avg_time

simulate_n_games(1000)