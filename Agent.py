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
            Compute the path from the snake's head to the apple using BFS,
            considering that the snake's tail moves over time.

            :param apple: Tuple (row, col) of the apple's position.
            :param snake: Snake object representing the current snake state.
            :return: List of directions ('up', 'down', 'left', 'right') to reach the apple.
        """

        head = snake.getHead()
        body = list(snake.getBody())  # keep order: head -> tail

        parent = {head: None}
        q = deque([(head, 0)])  # (position, depth)

        while q:
            (ci, cj), depth = q.popleft()

            for di, dj in moves:
                ni, nj = ci + di, cj + dj
                nxt = (ni, nj)

                # out of bounds
                if not (0 <= ni < self.rows and 0 <= nj < self.columns):
                    continue

                # simulate that the tail frees cells after `depth` moves
                if depth < len(body) - 1:
                    future_blocked = set(body[:len(body) - depth])
                else:
                    future_blocked = {head}

                if nxt in future_blocked or nxt in parent:
                    continue

                parent[nxt] = (ci, cj)
                if nxt == apple:
                    # reconstruct path
                    pathDirections = []
                    cur = apple

                    while cur != head:
                        pi, pj = parent[cur]
                        pathDirections.append(pathMap[(cur[0] - pi, cur[1] - pj)])
                        cur = (pi, pj)

                    pathDirections.reverse()
                    return pathDirections

                q.append(((ni, nj), depth + 1))

        return []  # no path found