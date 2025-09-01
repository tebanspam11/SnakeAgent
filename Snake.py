from collections import deque

class Snake:
    def __init__(self, body = [(7, 4), (7, 3), (7, 2), (7, 1)]):
        """
            Initialize the snake with its initial body.

            :param body: List of tuples representing the snake's segments (head first).
        """
        
        self.body = deque(body)

    def getHead(self):
        """
            Get the current head position.

            :return: Tuple (row, column) of the head.
        """
        
        return self.body[0]
    
    def getBody(self):
        """
            Get the full snake body.

            :return: List of tuples representing the body segments.
        """

        return list(self.body) 

    def move(self, next_position, grow = False):
        """
            Move the snake to the next position.

            :param next_position: Tuple (row, column) of the new head position.
            :param grow: Boolean, if True the snake grows; otherwise, the tail moves.
        """

        self.body.appendleft(next_position)

        if not grow:
            self.body.pop()