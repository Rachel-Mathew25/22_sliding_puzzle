import io, sys, builtins
from puzzle import Puzzle
from game import SlidingPuzzle

def inversions(flat):
    t=[x for x in flat if x]; return sum(1 for i in range(len(t)) for j in range(i+1,len(t)) if t[i]>t[j])
def solvable(p):
    n=p.size; inv=inversions(sum(p.board,[]))
    if n%2: return inv%2==0
    return (inv + (n - p.blank_pos()[0])) % 2 == 1

for n in (3,4,5):
    for _ in range(2000):
        p=Puzzle(n); assert solvable(p) and not p.solved()
print("1. solvability OK for 3/4/5 x2000")

p=Puzzle(3); p.board=p.solved_board()          # blank bottom-right
assert p.move("s") is False and p.move("d") is False and p.move("x") is False and p.move("") is False
print("2. impossible/invalid moves return False")

# game: invalid input, move counts, size selection (blank rigged to bottom-right corner)
g=SlidingPuzzle()
o=g.start_game
def rig(size):
    o(size); g.puzzle.board=g.puzzle.solved_board(); g.puzzle.move('a'); g.puzzle.move('a')   # blank bottom-left
g.start_game=rig
inputs=iter(["7","3","","wa","as","x","?","a","s","d"])   # bad size, size 3, junk, 2 illegal, 1 legal (d)
def fake(prompt=""):
    try: return next(inputs)
    except StopIteration: raise EOFError
builtins.input=fake
g.run()
assert g.size==3 and g.moves==1, (g.size,g.moves)
print("3. size choice works; '', 'wa', 'as', junk and illegal moves don't crash or count; 1 legal (d) move counted")

# solve a small board by reversing a known scramble
import time
g=SlidingPuzzle()
g.choose_size=lambda:3
orig=g.start_game
seq=["w","a","w","d"]; inv={"w":"s","s":"w","a":"d","d":"a"}
def rigged(size):
    orig(size); g.puzzle.board=g.puzzle.solved_board()
    for m in seq: assert g.puzzle.move(m)
g.start_game=rigged
inputs=iter([inv[m] for m in reversed(seq)]+["w","w"])   # extra 'w' must never be read
builtins.input=fake
g.run()
assert g.puzzle.solved() and g.moves==4 and g.finished is not None
assert next(inputs)=="w"                                  # game ended without consuming extra input
t=g.elapsed(); time.sleep(1.1); assert g.elapsed()==t
print("4. solved detected, moves=4, game ends cleanly, timer frozen")
