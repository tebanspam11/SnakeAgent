import random
import statistics  

from Snake import Snake
from Agent import Agent
from config import *

directionMap = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
pathMap = {(1, 0): "down", (0, 1): "right", (-1, 0): "up", (0, -1): "left"}

class Game:
    def __init__(self, rows, cols):
        """
            Initialize a new Snake game.

            :param rows: Number of rows in the game board.
            :param cols: Number of columns in the game board.
        """

        self.rows = rows
        self.cols = cols
        self.snake = Snake()
        self.apple = self.spawnApple()
        self.score = 0
        self.steps = 0

    def spawnApple(self):
        """
            Spawn an apple in a random free cell not occupied by the snake.

            :return: Tuple (row, col) of apple's position or None if no free cells.
        """

        free_cells = [
            (i, j) for i in range(self.rows) for j in range(self.cols)
            if (i, j) not in self.snake.getBody()
        ]
        return random.choice(free_cells) if free_cells else None

    def step(self, direction):
        """
            Advance the game by one move in the given direction.

            :param direction: String ('up', 'down', 'left', 'right') representing snake's move.
            :return: True if the snake is alive after the move, False if it collides.
        """

        head = self.snake.getHead()
        dx, dy = directionMap[direction]
        newHead = (head[0] + dx, head[1] + dy)

        if (newHead[0] < 0 or newHead[0] >= self.rows or
            newHead[1] < 0 or newHead[1] >= self.cols or
            newHead in self.snake.getBody()):
            return False

        if newHead == self.apple:
            self.snake.move(newHead, grow=True)
            self.apple = self.spawnApple()
            self.score += 1
        else:
            self.snake.move(newHead, grow=False)

        self.steps += 1
        return True


def simulate_once(rows, cols, agent, time_limit=120.0):
    """
        Simulate a single game using the provided agent.

        :param rows: Number of rows in the game board.
        :param cols: Number of columns in the game board.
        :param agent: Agent object to control the snake.
        :param time_limit: Maximum allowed time in seconds for the game.
        :return: Tuple (score, steps, time_survived, reached_time_limit)
    """

    game = Game(rows, cols)
    while True:
        current_time = game.steps * MOVE_INTERVAL
        if current_time >= time_limit:
            return game.score, game.steps, time_limit, True

        path = agent.compute(game.apple, game.snake)
        if not path:
            break

        for direction in path:
            alive = game.step(direction)
            if not alive:
                return game.score, game.steps, game.steps * MOVE_INTERVAL, False
            if game.steps * MOVE_INTERVAL >= time_limit:
                return game.score, game.steps, time_limit, True

    return game.score, game.steps, game.steps * MOVE_INTERVAL, False


def simulate_n_games(n, rows=ROWS, cols=COLUMNS, time_limit=120.0):
    """
        Simulate multiple games and report statistics.

        :param n: Number of games to simulate.
        :param rows: Number of rows in the game board.
        :param cols: Number of columns in the game board.
        :param time_limit: Maximum allowed time per game in seconds.
        :return: Tuple containing statistics:
                 (avg_score, std_score, min_score, max_score,
                  avg_time,  std_time,  min_time,  max_time,
                  percent_reached_limit)
    """

    agent = Agent(rows, cols)

    scores = []
    times = []
    games_reached_limit = 0

    for _ in range(n):
        score, steps, time_survived, reached_limit = simulate_once(rows, cols, agent, time_limit)
        scores.append(score)
        times.append(time_survived)
        if reached_limit:
            games_reached_limit += 1

    avg_score = statistics.mean(scores)
    avg_time  = statistics.mean(times)

    std_score = statistics.stdev(scores) if len(scores) > 1 else 0.0
    std_time  = statistics.stdev(times) if len(times) > 1 else 0.0

    min_score = min(scores)
    max_score = max(scores)
    min_time  = min(times)
    max_time  = max(times)

    percent_reached_limit = (games_reached_limit / n) * 100

    print(f"\nAfter {n} games (limit {time_limit}s):")
    print(f"  Average score: {avg_score:.2f}   Std dev: {std_score:.2f}")
    print(f"    Min score: {min_score}   Max score: {max_score}")
    print(f"  Average time:  {avg_time:.2f} s  Std dev: {std_time:.2f}")
    print(f"    Min time: {min_time:.2f} s   Max time: {max_time:.2f} s")
    print(f"  % games reaching {time_limit}s: {percent_reached_limit:.1f}%")

    return (avg_score, std_score, min_score, max_score,
            avg_time,  std_time,  min_time,  max_time,
            percent_reached_limit)

simulate_n_games(1000, time_limit=120.0)