import time

from Control import Control
from Image import Image
from Agent import Agent
from Snake import Snake

directionMap = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

class Environment:
    def __init__(self, rows, columns, tileSize, top, left, moveInterval):
        """
            Initialize the environment that orchestrates the game automation.

            :param rows: Number of rows in the board.
            :param columns: Number of columns in the board.
            :param tileSize: Size of each tile in pixels.
            :param top: Y-coordinate of the top-left corner of the board.
            :param left: X-coordinate of the top-left corner of the board.
            :param moveInterval: Time between moves in seconds.
        """
    
        self.control = Control()
        self.image = Image(rows, columns, tileSize, top, left)
        self.agent = Agent(rows, columns)
        self. snake = Snake()

        self.apple = None
        self.pathDirections = None
        self.nextMoveTime = None

        self.moveInterval = moveInterval

    def setApple(self):
        """
            Continuously search for the apple's position until found.
        """
        
        while not self.apple:
            self.apple = self.image.findApple()

    def updateSnake(self, direction):
        """
            Update the snake's position based on the given direction.

            :param direction: String representing the move direction.
        """

        headX, headY = self.snake.getHead()
        dx, dy = directionMap[direction]
        newHead = (headX + dx, headY + dy)
        self.snake.move(newHead, newHead == self.apple)

    def makeMove(self, direction):
        """
            Execute a move, ensuring consistent timing between moves.

            :param direction: String representing the move direction.
        """

        if not self.nextMoveTime: 
            self.control.makeMove(direction)
            self.nextMoveTime = time.time() + self.moveInterval
        else:
            while time.time() < self.nextMoveTime:
                time.sleep(0.05) 

            self.control.makeMove(direction)
            self.nextMoveTime += self.moveInterval

        self.updateSnake(direction)

    def play(self):
        """
            Start and continuously play the game using the agent's strategy.
        """
        
        self.control.start()
        time.sleep(0.5)

        while True:
            self.setApple()
            self.pathDirections = self.agent.compute(self.apple, self.snake)

            for direction in self.pathDirections:
                self.makeMove(direction)

            self.apple = None