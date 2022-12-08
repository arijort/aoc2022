#!/usr/bin/env python

import re

filename = "input.txt"

"""
After the rearrangement procedure completes, what crate ends up on top of each stack?

Input looks like this
                [M]     [V]     [L]
[G]             [V] [C] [G]     [D]
[J]             [Q] [W] [Z] [C] [J]
[W]         [W] [G] [V] [D] [G] [C]
[R]     [G] [N] [B] [D] [C] [M] [W]
[F] [M] [H] [C] [S] [T] [N] [N] [N]
[T] [W] [N] [R] [F] [R] [B] [J] [P]
[Z] [G] [J] [J] [W] [S] [H] [S] [G]
 1   2   3   4   5   6   7   8   9 

move 1 from 5 to 2
move 7 from 7 to 1
"""

def main(upd=False):
  num_stacks = 9 # ok to hardcode?
  stacks = [ [] for s in range(num_stacks) ]
  with open(filename, "r") as fh:
    for line in fh:
      stack_match = re.match(r".(.)...(.)...(.)...(.)...(.)...(.)...(.)...(.)...(.).", line) # bug if last col isn't full?
      if stack_match:
        [ stacks[n].insert(0, stack_match.group(n+1)) for n in range(num_stacks) if stack_match.group(n+1).isalpha() ]
      move_match = re.match(r"move (\d+) from (\d+) to (\d+)", line)
      if move_match:
        num = int(move_match.group(1))
        frm = int(move_match.group(2)) - 1
        to  = int(move_match.group(3)) - 1
        if not upd:
          [ stacks[to].append( stacks[frm].pop() ) for _ in range(num) ]
        else:
          stacks[to].extend(stacks[frm][-num:])
          stacks[frm] = stacks[frm][0:-num]

  result = "".join([ stacks[s][-1] for s in range(num_stacks) ])
  print(f"result is {result}")

if __name__ == "__main__":
  main()
  main(upd=True)
