#!/usr/local/bin/python3.11

import sys
import numpy as np
filename = "input.txt"
#filename = "small"

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
  global max_x, min_x, max_y, min_y
  #print(f"adding point {x},{y}")
  max_x = max(max_x, x)
  max_y = max(max_y, y)
  min_x = min(min_x, x)
  min_y = min(min_y, y)
  s.add( (x,y) )

def draw(points, h, t):
  """ Take the set of points we are tracking and draw graph."""
  global max_x, min_x, max_y, min_y
  bound_x = ( min(min_x, -5), max(max_x + 2, 5) )
  bound_y = ( min(min_y, -5), max(max_y + 2, 5) )
  #print(f"drawing from x {bound_x[0]} to {bound_x[1]} and y {bound_y[0]} to {bound_y[1]}")
  #print(f"  have points {points}")
  for y in range(bound_y[1], bound_y[0], -1):
    for x in range(bound_x[0] , bound_x[1]):
      if (x,y) == (0,0):
        print("s", end="")
      elif (x,y) == h:
        print("H", end="")
      elif (x,y) == t:
        print("T", end="")
      elif (x,y) in points:
        print("*", end="")
      elif (x,y) == (0,0):
        print("s", end="")
      else:
        print(".", end="")
    print("\n", end="")

def point_chase(h, t, s, track=False):
  """ Calculate path tail follows when chasing head. Use track boolean to drive whether to return list of points that tail follows. """
  # case 1: no T movement because of adjacency
  if are_adjacent(h, t):
    print("case 1 no movement")
  # case 2: no T movement because of overlapping
  elif are_overlapping(h, t):
    print("case 2 no movement")
  # case 3: T moves in 1 dimension y; because x matches 
  elif h[0] == t[0]:
    print("case 3 movement along y")
    cmp = compare( t[1], h[1])
    #for y in range( min( h[1], t[1]) , max( h[1], t[1]) ):
    for y in range( t[1], h[1], cmp ):
      if track: add_point(s, t[0], y)
    t = (t[0], y)
  # case 4: T moves in 1 dimension x; because y matches
  elif h[1] == t[1]:
    print("case 4 movement along x")
    cmp = compare( t[0], h[0]) 
    for x in range( t[0], h[0], cmp ):
      if track: add_point(s, x, t[1])
      t = (x, t[1])
  else:
    # case 5 T mvoes diagonally
    print(f"case 5 diagonal movement from tail {t} to head {h}")
    while not are_adjacent(h, t):
      delta_x = compare( t[0], h[0] )
      delta_y = compare( t[1], h[1] )
      t = (t[0] + delta_x, t[1] + delta_y )
      if track: add_point(s, t[0], t[1])
  return (t,s)

def pull(pulls):
  s = set() # track points visited by tail in tuples (x,y)
  initx, inity = 0, 0
  h, t = (initx, inity), (initx, inity)
  num_knots = 9
  knots = [ (initx, inity) ] * 9
  add_point(s, initx, inity)
  for direction, amount in pulls: # each pulls is direction and amount e.g. R 4
    vec = np.array(directions[direction]) * int(amount)
    #h = (h[0] + vec[0] , h[1] + vec[1] )
    h = (h[0] + vec[0] , h[1] + vec[1] )
    print(f"have movement '{direction} {amount}' vec {vec} to {h} with tail {t}")
    #print(f"tail {t} chasing new h {h} ")
    (t,s) = point_chase(h, t, s, True)
    print(f"tail ending at {t} chasing h {h} ")
    #draw(s, h, t)
  return len(s)

def main():
  pulls = []
  with open(filename, "r") as fh:
    for line in fh:
      pulls.append( (line.strip().split() ) ) # unpack tuple straight into function call

  result = pull(pulls)
  print (f"part 1 result is {result}") # should be 6354

if __name__ == "__main__":
  main()
