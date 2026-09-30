import random

DIRECTIONS = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
OPPOSITE = {"w": "s", "s": "w", "a": "d", "d": "a"}
VALID_SIZES = (3, 4, 5)


class Puzzle:
    def __init__(self, size=4):
        if size not in VALID_SIZES:
            raise ValueError(f"size must be one of {VALID_SIZES}")
        self.size = size
        self.board = self.solved_board()
        self.scramble()

    def solved_board(self):
        tiles = list(range(1, self.size * self.size)) + [0]
        return [tiles[r * self.size:(r + 1) * self.size] for r in range(self.size)]

    def scramble(self, steps=None):
        """Start from the solved board and apply random LEGAL blank moves,
        so every generated board is reachable (correct parity)."""
        steps = steps or self.size * self.size * 20
        self.board = self.solved_board()
        last = None
        for _ in range(steps):
            options = [d for d in DIRECTIONS
                       if self._target(d) is not None and d != OPPOSITE.get(last)]
            last = random.choice(options)
            self._swap(last)
        if self.solved():          # extremely unlikely, but never start solved
            self.scramble(steps)

    def blank_pos(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c

    def _target(self, direction):
        r, c = self.blank_pos()
        dr, dc = DIRECTIONS[direction]
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.size and 0 <= nc < self.size:
            return nr, nc
        return None

    def _swap(self, direction):
        r, c = self.blank_pos()
        nr, nc = self._target(direction)
        self.board[r][c], self.board[nr][nc] = self.board[nr][nc], self.board[r][c]

    def move(self, direction):
        """Move the blank one step. Returns True only if a tile actually moved."""
        if direction not in DIRECTIONS or self._target(direction) is None:
            return False
        self._swap(direction)
        return True

    def solved(self):
        return self.board == self.solved_board()
