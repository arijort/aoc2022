#!/usr/local/bin/python3.11

import sys
from pprint import pprint
from enum import Enum
import math
import numpy as np
filename = "input.txt"
#filename = "small"

class TreeVis(Enum):
  LEFT = 0
  TOP = 1
  BOTTOM = 2
  RIGHT = 3

"""
Part 1:

  Inspect a grid of integers representing tree heights. Example here:

  30373
  25512
  65332
  33549
  35390
  
  Find number of trees visible to the exterior. This number will include *all* trees on perimeter plus 
  internal trees high enough to be visible from at least one edge.

input is 99x99 grid
"""

def check_scenic(row,col,hgt, scenic, left,up,down,right):
  # check each direction
  for direction, idx in zip([left, right, up, down], [TreeVis.LEFT, TreeVis.RIGHT, TreeVis.TOP, TreeVis.BOTTOM]):
    tree_count = 0
    for tree in direction:
      tree_count += 1
      if tree >= hgt: break
    scenic[row][col][idx.value] = tree_count
  return scenic

# compare height of focal point tree to each tree in line of 4 compass directions
def check_cell(row,col,hgt,vis, left, up, down, right):
  for direction, idx in zip([left, right, up, down], [TreeVis.LEFT, TreeVis.RIGHT, TreeVis.TOP, TreeVis.BOTTOM]):
    vis[row][col][idx.value] = max(direction) < hgt # check all trees are lower than focal point
  return vis

def main():
  mat = []
  with open(filename, "r") as fh:
    for line in fh:
      mat.append( list(line.strip()) )
  vis = [[[ True for _ in range(len(TreeVis))] for _ in range(len(mat[0])) ] for _ in  range(len(mat)) ]
  scenic = [[[ 0 for _ in range(len(TreeVis))] for _ in range(len(mat[0])) ] for _ in  range(len(mat)) ]
  npmat = np.array(mat)
 
  # exclude edges; start with 1
  for r in range(1,len(mat)-1) :
    for c in range(1,len(mat[0]) - 1):

      left  = np.flip(npmat[r,   0:c ])
      up    = np.flip(npmat[0:r, c   ])
      right =         npmat[r,   c+1:]
      down  =         npmat[r+1:,c   ]

      vis    = check_cell(  r,c,mat[r][c],vis,    left, up, down, right)
      scenic = check_scenic(r,c,mat[r][c],scenic, left, up, down, right)

  result = sum([ any(c) for r in vis for c in r ])
  print (f"part 1 result len is {result}")
  result2 = max( [ math.prod(c) for r in scenic for c in r ] )
  print (f"part 2 result is {result2}") # should be 410400

if __name__ == "__main__":
  main()
