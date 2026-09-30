import time
from puzzle import Puzzle, VALID_SIZES


class SlidingPuzzle:
    def __init__(self):
        self.size = 4
        self.puzzle = None
        self.moves = 0
        self.started = None
        self.finished = None   # frozen end time once solved

    def choose_size(self):
        while True:
            try:
                raw = input(f"Board size {VALID_SIZES} [default 4]: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                raise SystemExit
            if raw == "":
                return 4
            if raw in ("3", "4", "5"):
                return int(raw)
            print("Please enter 3, 4 or 5.")

    def start_game(self, size):
        """Session values (moves, timer) are reset here and ONLY here."""
        self.size = size
        self.puzzle = Puzzle(size)
        self.moves = 0
        self.started = time.monotonic()
        self.finished = None

    def elapsed(self):
        end = self.finished if self.finished is not None else time.monotonic()
        return int(end - self.started)

    def display(self):
        width = len(str(self.size * self.size - 1))
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or '':>{width}}" for x in row))
        print("Moves:", self.moves, " Time:", self.elapsed(), "s")

    def run(self):
        print("Sliding Puzzle — W/A/S/D moves the blank up/left/down/right. Q quits.")
        self.start_game(self.choose_size())
        while True:
            self.display()
            if self.puzzle.solved():
                print(f"Solved in {self.moves} moves and {self.elapsed()} s!")
                return
            try:
                key = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if key == "q":
                return
            if key not in ("w", "a", "s", "d"):
                print("Use W/A/S/D (or Q to quit).")
                continue
            if self.puzzle.move(key):
                self.moves += 1
                if self.puzzle.solved():
                    self.finished = time.monotonic()   # freeze before the redraw
            else:
                print("That move is not possible.")
