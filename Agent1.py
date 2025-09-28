from collections import deque
import heapq

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

    def _a_star(self, target, snake, inverse=False):
        head = snake.getHead()
        body = list(snake.getBody())
        open_set = []
        heapq.heappush(open_set, (0 + self._manhattan(head, target), 0, head, [head]))
        visited = {head}

        if inverse:
            target = snake.getBody()[-1]

        while open_set:
            f, g, current, path = heapq.heappop(open_set)
            if current == target:
                moves_path = []
                for i in range(1, len(path)):
                    di, dj = path[i][0]-path[i-1][0], path[i][1]-path[i-1][1]
                    moves_path.append(pathMap[(di,dj)])
                return moves_path, len(moves_path)

            for di, dj in moves:
                ni, nj = current[0]+di, current[1]+dj
                nxt = (ni,nj)
                if self._is_valid_move(nxt, snake, g, body, {} ) and nxt not in visited:
                    visited.add(nxt)

                    if inverse:
                    # heurística inversa: maximizar distancia al objetivo para alargar camino
                        h = -self._manhattan(nxt, target)
                    else:
                        h = self._manhattan(nxt, target)

                    heapq.heappush(open_set, (g+1+h, g+1, nxt, path+[nxt]))

        return [], 0


    def _manhattan(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
    
    def compute(self, apple, snake):
        snake_len = len(snake.getBody())
        total_cells = self.rows * self.columns
        dynamic_threshold = 0.5 + 0.4 * (snake_len / total_cells)
        candidates = []

    # Helper: simular camino con +1 paso de crecimiento
        def simulate_with_growth(path):
            body = list(snake.getBody())
            for step in path:
                di, dj = next(k for k, v in pathMap.items() if v == step)
                new_head = (body[0][0] + di, body[0][1] + dj)
                body.insert(0, new_head)
                if new_head == apple:
                    pass  # aquí crecería (no hacemos pop)
                else:
                    body.pop()
            return body

    #BFS normal
        bfs_path, bfs_len = self._find_path(apple, snake, use_body_hugging=False)
        if bfs_path:
            body = simulate_with_growth(bfs_path)
            if self.has_safe_space(body, threshold=dynamic_threshold):
                candidates.append((bfs_path, bfs_len, 'BFS'))

    #BFS body hugging
        body_path, body_len = self._find_path(apple, snake, use_body_hugging=True)
        if body_path:
            body = simulate_with_growth(body_path)
            if self.has_safe_space(body, threshold=dynamic_threshold - 0.05):
                candidates.append((body_path, body_len, 'BFS body'))

    #A* normal
        astar_path, astar_len = self._a_star(apple, snake, inverse=False)
        if astar_path:
            body = simulate_with_growth(astar_path)
            if self.has_safe_space(body, threshold=dynamic_threshold + 0.05):
                candidates.append((astar_path, astar_len, 'A*'))

    #A* inverso (si cubre mas del 50%)
        if snake_len > (total_cells * 0.5):
            astar_inv_path, astar_inv_len = self._a_star(apple, snake, inverse=True)
            if astar_inv_path:
                body = simulate_with_growth(astar_inv_path)
                if self.has_safe_space(body, threshold=dynamic_threshold):
                    candidates.append((astar_inv_path, astar_inv_len, 'A* inverso'))

        if candidates:
            def score(entry):
                path, length, tag = entry
                priority_map = {'BFS': 0, 'A*': 1, 'BFS body': 2, 'A* inverso': 3}
                return (length, -priority_map[tag])  # más largo = mejor, menor prioridad = mejor

            candidates.sort(key=score, reverse=True)
            return candidates[0][0]

    # ---- Plan B: seguir cola ----
        tail_path = self._follow_tail(snake)
        if tail_path:
            return tail_path

    # Extra fallback: moverse a celda libre cercana
        for di, dj in moves:
            ni, nj = snake.getHead()[0] + di, snake.getHead()[1] + dj
            if 0 <= ni < self.rows and 0 <= nj < self.columns:
                if (ni, nj) not in snake.getBody():
                    return [pathMap[(di, dj)]]

        return []