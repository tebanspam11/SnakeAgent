from collections import deque
import heapq

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

    def _is_adjacent_to_body(self, pos, snake):
        """
            Check if a given position is adjacent to the snake's body (excluding the head).

            :param pos: Tuple (row, col) of the position to check.
            :param snake: Snake object representing the current snake state.
            :return: True if the position is adjacent to the body, False otherwise.
        """

        body = set(snake.getBody())
        body.discard(snake.getHead())
        for i, j in body:
            for di, dj in moves:
                if (i + di, j + dj) == pos:
                    return True
        return False

    def _is_valid_move(self, pos, snake, depth, body, parent):
        """
            Check if a move is valid (inside the board, not colliding with the body or parent path).

            :param pos: Tuple (row, col) of the position to check.
            :param snake: Snake object representing the current snake state.
            :param depth: Current depth in path exploration.
            :param body: List of snake body positions.
            :param parent: Dictionary of visited positions in current path.
            :return: True if the move is valid, False otherwise.
        """

        ni, nj = pos
        if not (0 <= ni < self.rows and 0 <= nj < self.columns):
            return False
        if depth < len(body) - 1:
            future_blocked = set(body[:len(body) - depth])
        else:
            future_blocked = {snake.getHead()}
        return pos not in future_blocked and pos not in parent

    def _manhattan(self, a, b):
        """
            Compute the Manhattan distance between two positions.

            :param a: Tuple (row, col) of the first position.
            :param b: Tuple (row, col) of the second position.
            :return: Manhattan distance between a and b.
        """

        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def _reachable_ratio(self, new_snake_body):
        """
            Compute the ratio of reachable free cells from the snake's head.

            :param new_snake_body: List of tuples representing the new snake body.
            :return: Ratio of reachable free cells to total free cells.
        """

        head = new_snake_body[0]
        body_set = set(new_snake_body)
        visited = {head}
        q = deque([head])

        while q:
            x, y = q.popleft()
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.rows and 0 <= ny < self.columns
                        and (nx, ny) not in body_set
                        and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    q.append((nx, ny))

        total_free = self.rows * self.columns - len(new_snake_body)
        return len(visited) / max(1, total_free)

    def _find_path(self, target, snake, use_body_hugging):
        """
            BFS-based pathfinding from the snake's head to a target position.

            :param target: Tuple (row, col) of the target position.
            :param snake: Snake object representing the current snake state.
            :param use_body_hugging: Boolean, whether to prioritize moves adjacent to the body.
            :return: Tuple (path as list of directions, path length)
        """

        head = snake.getHead()
        body = list(snake.getBody())
        parent = {head: None}
        q = deque([(head, 0)])

        while q:
            (ci, cj), depth = q.popleft()
            if (ci, cj) == target:
                path = []
                cur = target
                while cur != head:
                    pi, pj = parent[cur]
                    path.append(pathMap[(cur[0] - pi, cur[1] - pj)])
                    cur = (pi, pj)
                path.reverse()
                return path, len(path)

            neighbors = []
            if use_body_hugging:
                high, low = [], []
                for di, dj in moves:
                    ni, nj = ci + di, cj + dj
                    nxt = (ni, nj)
                    if self._is_valid_move(nxt, snake, depth, body, parent):
                        (high if self._is_adjacent_to_body(nxt, snake) else low).append(nxt)
                neighbors = high + low
            else:
                for di, dj in moves:
                    ni, nj = ci + di, cj + dj
                    nxt = (ni, nj)
                    if self._is_valid_move(nxt, snake, depth, body, parent):
                        neighbors.append(nxt)

            for nxt in neighbors:
                if nxt not in parent:
                    parent[nxt] = (ci, cj)
                    q.append((nxt, depth + 1))

        return [], 0

    def _a_star(self, target, snake):
        """
            A* pathfinding algorithm from the snake's head to a target position.

            :param target: Tuple (row, col) of the target position.
            :param snake: Snake object representing the current snake state.
            :param inverse: Boolean, if True, compute path to tail instead of apple.
            :return: Tuple (path as list of directions, path length)
        """

        head = snake.getHead()
        body = list(snake.getBody())
        open_set = []
        heapq.heappush(open_set, (0 + self._manhattan(head, target), 0, head, [head]))
        visited = {head}

        while open_set:
            f, g, current, path = heapq.heappop(open_set)
            if current == target:
                moves_path = []
                for i in range(1, len(path)):
                    di, dj = path[i][0]-path[i-1][0], path[i][1]-path[i-1][1]
                    moves_path.append(pathMap[(di, dj)])
                return moves_path, len(moves_path)

            for di, dj in moves:
                ni, nj = current[0] + di, current[1] + dj
                nxt = (ni, nj)
                if self._is_valid_move(nxt, snake, g, body, {}) and nxt not in visited:
                    visited.add(nxt)
                    h = self._manhattan(nxt, target)
                    heapq.heappush(open_set, (g + 1 + h, g + 1, nxt, path + [nxt]))

        return [], 0

    def _follow_tail(self, snake):
        """
            Compute a path to the snake's tail.

            :param snake: Snake object representing the current snake state.
            :return: List of directions to follow the tail.
        """

        tail = snake.getBody()[-1]
        return self._find_path(tail, snake, use_body_hugging=False)[0]

    def compute(self, apple, snake):
        """
            Compute the path from the snake's head to the apple using BFS,
            considering that the snake's tail moves over time.

            :param apple: Tuple (row, col) of the apple's position.
            :param snake: Snake object representing the current snake state.
            :return: List of directions ('up', 'down', 'left', 'right') to reach the apple.
        """

        snake_len = len(snake.getBody())
        total_cells = self.rows * self.columns
        dynamic_threshold = 0.4 + 0.4 * (snake_len / total_cells)
        candidates = []

        def simulate_with_growth(path):
            body = list(snake.getBody())
            for step in path:
                di, dj = next(k for k, v in pathMap.items() if v == step)
                new_head = (body[0][0] + di, body[0][1] + dj)
                body.insert(0, new_head)
                if new_head != apple:
                    body.pop()
            return body

        checks = [
            ("BFS", lambda: self._find_path(apple, snake, use_body_hugging=False)),
            ("BFS body", lambda: self._find_path(apple, snake, use_body_hugging=True)),
            ("A*", lambda: self._a_star(apple, snake)),
        ]
        for tag, finder in checks:
            path, length = finder()
            if path:
                body = simulate_with_growth(path)
                if self._reachable_ratio(body) >= dynamic_threshold:
                    ratio = self._reachable_ratio(body)
                    candidates.append((path, length, ratio, tag))

        if candidates:
            def score(entry):
                path, length, ratio, _ = entry
                norm_len = length / (self.rows * self.columns)
                return 0.5 * ratio + 0.5 * (1 - norm_len) 
            best = max(candidates, key=score)
            return best[0]

        tail_path = self._follow_tail(snake)
        if tail_path:
            return tail_path

        for di, dj in moves:
            ni, nj = snake.getHead()[0] + di, snake.getHead()[1] + dj
            if 0 <= ni < self.rows and 0 <= nj < self.columns:
                if (ni, nj) not in snake.getBody():
                    return [pathMap[(di, dj)]]

        return []