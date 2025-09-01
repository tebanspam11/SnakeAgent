from collections import deque

moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
pathMap = {(1, 0): "down", (0, 1): "right", (-1, 0): "up", (0, -1): "left"}
    
class Agent:
    def __init__(self, rows, columns):
        """
            Initialize the agent with the board dimensions.

            :param rows: Number of rows in the board.
            :param columns: Number of columns in the board.
        """

        self.rows = rows
        self.columns = columns

    def compute(self, apple, snake):
        """
            Compute the path from the snake's head to the apple using BFS.

            :param apple: Tuple (row, col) of the apple's position.
            :param snake: Snake object representing the current snake state.
            :return: List of directions ('up', 'down', 'left', 'right') to reach the apple.
        """

        parent = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        head = snake.getHead()
        body = set(snake.getBody())

        q = deque([head])

        while q:
            ci, cj = q.popleft()

            for di, dj in moves:
                ni, nj = ci + di, cj + dj

                if 0 <= ni < self.rows and 0 <= nj < self.columns and parent[ni][nj] is None and (ni, nj) not in body:
                    parent[ni][nj] = (ci, cj)
                    q.append((ni, nj))

        pathDirections = []
        cur = apple

        while cur != head:
            pi, pj = parent[cur[0]][cur[1]]
            pathDirections.append(pathMap[(cur[0] - pi, cur[1] - pj)])
            cur = (pi, pj)

        pathDirections.reverse()
        return pathDirections