from collections import deque

moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
pathMap = {(1, 0): "down", (0, 1): "right", (-1, 0): "up", (0, -1): "left"}

class Agent:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def is_adjacent_to_body(self, pos, snake):
        body = set(snake.getBody())
        body.discard(snake.getHead())
        for i, j in body:
            for di, dj in moves:
                if (i + di, j + dj) == pos:
                    return True
        return False

    def _find_path(self, target, snake, use_body_hugging):
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
                        if self.is_adjacent_to_body(nxt, snake):
                            high.append(nxt)
                        else:
                            low.append(nxt)
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

    def _is_valid_move(self, pos, snake, depth, body, parent):
        ni, nj = pos
        if not (0 <= ni < self.rows and 0 <= nj < self.columns):
            return False
        if depth < len(body) - 1:
            future_blocked = set(body[:len(body) - depth])
        else:
            future_blocked = {snake.getHead()}
        return pos not in future_blocked and pos not in parent

    def has_safe_space(self, new_snake_body, threshold=0.6):
        """
        Comprueba que desde la nueva cabeza se pueda llegar
        al menos a un % de las celdas libres (threshold).
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
        return len(visited) >= max(5, int(total_free * threshold))

    def simulate_path(self, snake, path):
        body = list(snake.getBody())
        for step in path:
            di, dj = next(k for k, v in pathMap.items() if v == step)
            new_head = (body[0][0] + di, body[0][1] + dj)
            body.insert(0, new_head)
            body.pop()  # no crecimiento hasta comer
        return body

    def _follow_tail(self, snake):
        """
        Plan B: buscar camino hasta la cola actual.
        """
        tail = snake.getBody()[-1]
        return self._find_path(tail, snake, use_body_hugging=False)[0]

    def compute(self, apple, snake):
        shortest_path, shortest_len = self._find_path(apple, snake, use_body_hugging=False)
        if not shortest_path:
            return self._follow_tail(snake) or []

        body_hugging_path, hug_len = self._find_path(apple, snake, use_body_hugging=True)
        candidate = body_hugging_path if hug_len > 0 and hug_len == shortest_len else shortest_path

        # Comprobación solo al final y con umbral
        simulated_body = self.simulate_path(snake, candidate)
        if self.has_safe_space(simulated_body, threshold=0.5):
            return candidate

        # Intentar el otro camino
        if candidate != shortest_path:
            simulated_body = self.simulate_path(snake, shortest_path)
            if self.has_safe_space(simulated_body, threshold=0.5):
                return shortest_path

        # Plan B: seguir la cola para ganar tiempo
        return self._follow_tail(snake) or []