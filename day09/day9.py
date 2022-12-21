#!/usr/local/bin/python3.11

import os
filename = "input.txt" # 2629 too low 2868 too high; should be 2651
#filename = "small"
#filename = "medium"

"""
Part 1:

  Assume a rope with a head H and tail T. Both head and tail start at the same point (overlapping)
  Receive as input a set of instructions indicating where the head is moved, up, down, left, right.
  Tail follows the head, they must always be adjacent. Diagonally counts as adjacent.
  If head movement pulls tail such they are in different rows and cols, then T moves diagonally to catch up to H. 

    R 4
    U 4
    L 3
    D 1
    R 4
    D 1
    L 5
    R 2

input is 2000 instructions

Part 2: assume 10 knots. Track the last knot.
"""

xdirections = { 'R': 1, 'L': -1, 'U': 0, 'D': 0  }
ydirections = { 'R': 0, 'L': 0,  'U': 1, 'D': -1 }

def compare(a, b):
  """ Like spaceship comparison operation: return 0 if equal; -1 if a > b; and 1 if a < b """
  if a == b:
    return 0
  elif a < b:
    return 1
  else:
    return -1

def are_adjacent(head, tail):
  return abs( head[0] - tail[0] ) < 2 and abs( head[1] - tail[1]) < 2

max_x, min_x, max_y, min_y = 0,0,0,0

def draw(points, knots):
  """ Take the set of points we are tracking and draw graph."""
  os.system("clear")
  global max_x, min_x, max_y, min_y
  bound_x = ( min(min_x-1, -5), max(max_x + 1, 5) )
  bound_y = ( min(min_y-1, -5), max(max_y + 1, 5) )
  kd = { k:n for n,k in enumerate(knots) }
  for y in reversed(range(bound_y[1], bound_y[0])): # go in reverse to make up appear up
    for x in range(bound_x[0] , bound_x[1]):
      if (x,y) == (0,0):
        print("s", end="")
      elif (x,y) == knots[0]:
        print("H", end="")
      elif (x,y) == knots[ len(knots) - 1]:
        print("T", end="")
      elif (x,y) in points:
        print("*", end="")
      elif (x,y) in knots:
        print(f"{kd[(x,y)]}", end="")
      else:
        print(".", end="")
    print("\n", end="")

def point_chase(h, t):
  """ Calculate path tail follows when chasing head. """
  while not are_adjacent(h, t):
    delta_x = compare( t[0], h[0] )
    delta_y = compare( t[1], h[1] )
    t = (t[0] + delta_x, t[1] + delta_y )
  return t

def pull(pulls):
  s1, s2 = set(), set() # track points visited by tail in tuples (x,y)
  npull, initx, inity = 0, 0, 0
  num_knots = 10
  knots = [ (initx, inity) ] * num_knots
  s1.add( (initx, inity) )
  s2.add( (initx, inity) )
  for npull, (direction, amount) in enumerate(pulls): # each pulls is direction and amount e.g. R 4
    global max_x, min_x, max_y, min_y
    max_x, max_y = max(max_x, knots[0][0]), max(max_y, knots[0][1])
    min_x, min_y = min(min_x, knots[0][0]), min(min_y, knots[0][1])
    for step in range(int(amount)):
      knots[0] = (knots[0][0] + xdirections[direction] , knots[0][1] + ydirections[direction] )
      for k in range(1, num_knots):
        knots[k] = point_chase(knots[k-1], knots[k] )
      #draw(s2, knots)
      s1.add( knots[1] ) # track second knot
      s2.add( knots[-1] ) # track last knot
  return (len(s1), len(s2) )

def main():
  pulls = []
  with open(filename, "r") as fh:
    for line in fh:
      pulls.append( (line.strip().split() ) ) # unpack tuple straight into function call

  r1, r2 = pull(pulls)
  print (f"part 1 result is {r1}") # should be 6354 for part 1
  print (f"part 2 result is {r2}") # should be 2651 for part 2

if __name__ == "__main__":
  main()
