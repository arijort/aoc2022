#!/usr/local/bin/python3.11

import sys
import numpy as np
filename = "input.txt" # 2629 too low 2868 too high
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
"""

directions = { 'R': (1,0), 'L': (-1,0), 'U': (0,1), 'D': (0, -1) }

def compare(a, b):
  """ Like spaceship comparison operation: return 0 if equal; -1 if a > b; and 1 if a < b """
  if a == b:
    return 0
  elif a < b:
    return 1
  else:
    return -1

def are_overlapping(head, tail):
  return head == tail

def are_adjacent(head, tail):
  return abs( head[0] - tail[0] ) < 2 and abs( head[1] - tail[1]) < 2

max_x, min_x, max_y, min_y = 0,0,0,0

def add_point(s, x, y):
  """ Add given point (x,y) to set of points (s) and track the min and max values of both x and y to allow for easy visualization """
  #print(f"adding point {x},{y}")
  s.add( (x,y) )

def draw(points, knots):
  """ Take the set of points we are tracking and draw graph."""
  global max_x, min_x, max_y, min_y
  bound_x = ( min(min_x-2, -5), max(max_x + 2, 5) )
  bound_y = ( min(min_y-2, -5), max(max_y + 2, 5) )
  kd = {}
  for n, k in enumerate(knots):
    kd[k] = n
  #print(f"drawing from x {bound_x[0]} to {bound_x[1]} and y {bound_y[0]} to {bound_y[1]}")
  #print(f"  have points {points}")
  for y in range(bound_y[1], bound_y[0], -1): # go in reverse to make up appear up
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

def point_chase(h, t, s, track=False):
  """ Calculate path tail follows when chasing head. Use track boolean to drive whether to return list of points that tail follows. """
  while not are_adjacent(h, t):
    delta_x = compare( t[0], h[0] )
    delta_y = compare( t[1], h[1] )
    t = (t[0] + delta_x, t[1] + delta_y )
    if track: add_point(s, t[0], t[1])
  return (t,s)

def pull(pulls):
  s = set() # track points visited by tail in tuples (x,y)
  npull, initx, inity = 0, 0, 0
  h, t = (initx, inity), (initx, inity)
  num_knots = 10
  knots = [ (initx, inity) ] * num_knots
  add_point(s, initx, inity)
  for direction, amount in pulls: # each pulls is direction and amount e.g. R 4
    vec = np.array(directions[direction]) * int(amount)
    knots[0] = (knots[0][0] + vec[0] , knots[0][1] + vec[1] )
    #print(f"pull {npull} have movement '{direction} {amount}' vec {vec} to {knots[0]}")
    global max_x, min_x, max_y, min_y
    max_x = max(max_x, knots[0][0])
    max_y = max(max_y, knots[0][1])
    min_x = min(min_x, knots[0][0])
    min_y = min(min_y, knots[0][1])
    for k in range(1, num_knots):
      h = knots[k - 1]
      t = knots[k]
      #print(f"k{k} at {t} chasing k{k-1} at {h}")
      tracker = (k == num_knots - 1)
      (t,s) = point_chase(h, t, s, tracker)
      #print(f"  moved to {t}")
      knots[k] = t
      #draw(s, knots)
    #print(f"tail ending at {t} chasing h {knots[0]} with {len(s)} visited: {s}")
    npull += 1
  return len(s)

def main():
  pulls = []
  with open(filename, "r") as fh:
    for line in fh:
      pulls.append( (line.strip().split() ) ) # unpack tuple straight into function call

  result = pull(pulls)
  print (f"part 1 result is {result}") # should be 6354 for part 1

if __name__ == "__main__":
  main()
