#!/usr/local/bin/python3.11

import sys
from pprint import pprint
from enum import Enum
#from functools import reduce
import itertools
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

def check_scenic(row,col,graph, scenic, left,up,down,right):
  #check each direction
  for direction, idx in zip([left, right, up, down], [TreeVis.LEFT, TreeVis.RIGHT, TreeVis.TOP, TreeVis.BOTTOM]):
    max_hgt, tree_count = -1, 0
    for tree in direction:
      if int(tree) > max_hgt:
        tree_count += 1
        max_hgt = max(max_hgt, int(tree))
      else:
        break
    scenic[row][col][idx.value] = tree_count
    return scenic
  #for r in range(row-1,-1,-1): # if row is 0 this loop will be empty
  #  if int(graph[r][col]) > max_hgt:
  #    tree_count += 1
  #    max_hgt = max(max_hgt, int(graph[r][col]))
  #  else:
  #    break
  #scenic[row][col][TreeVis.TOP.value] = tree_count

  #check downwards
def not_called():
  max_hgt, tree_count = -1, 0
  for r in range(row+1, len(graph)): # if row is 0 this loop will be empty
    if int(graph[r][col]) > max_hgt:
      tree_count += 1
      max_hgt = max(max_hgt, int(graph[r][col]))
    else:
      break
  scenic[row][col][TreeVis.BOTTOM.value] = tree_count

  # check left
  max_hgt, tree_count = -1, 0
  for c in range(col-1, -1, -1):
    if int(graph[row][c]) > max_hgt:
      tree_count += 1
      max_hgt = max(max_hgt, int(graph[row][c]))
    else:
      break
  scenic[row][col][TreeVis.LEFT.value] = tree_count

  # check right
  max_hgt, tree_count = -1, 0
  for c in range(col+1,len(graph[0])):
    if int(graph[row][c]) > max_hgt:
      tree_count += 1
      max_hgt = max(max_hgt, int(graph[row][c]))
    else:
      break
  scenic[row][col][TreeVis.RIGHT.value] = tree_count
  return scenic

def check_cell(row,col,graph,vis, left, up, down, right):
  for direction, idx in zip([left, right, up, down], [TreeVis.LEFT, TreeVis.RIGHT, TreeVis.TOP, TreeVis.BOTTOM]):
    vis[row][col][idx.value] = all( [ t < graph[row][col] for t in direction ] )
    #for t in direction:
    #  if t >= graph[row][col]:
    #    vis[row][col][idx.value] = False
    #    break
  return vis

def check_cell_old(row,col,graph,vis):
  #check top
  for r in range(row):
    if graph[r][col] >= graph[row][col]:
      vis[row][col][TreeVis.TOP.value] = False
      break
  # check bottom
  for r in range(row+1,len(graph)):
    if graph[r][col] >= graph[row][col]:
      vis[row][col][TreeVis.BOTTOM.value] = False
      break

  # check left
  for c in range(col):
    if graph[row][c] >= graph[row][col]:
      vis[row][col][TreeVis.LEFT.value] = False
      break
  # check right
  for c in range(col+1,len(graph[0])):
    if graph[row][c] >= graph[row][col]:
      vis[row][col][TreeVis.RIGHT.value] = False
      break
  return vis

def main():
  result = 0
  mat = []
  with open(filename, "r") as fh:
    for line in fh:
      mat.append( list(line.strip()) )
  vis = [[[ True for _ in range(len(TreeVis))] for _ in range(len(mat[0])) ] for _ in  range(len(mat)) ]
  scenic = [[[ 0 for _ in range(len(TreeVis))] for _ in range(len(mat[0])) ] for _ in  range(len(mat)) ]
  npmat = np.array(mat)
 
  # exclude edges
  for r in range(1,len(mat)-1) :
    for c in range(1,len(mat[0]) - 1):

      left  = np.flip(npmat[r, 0:c ])
      up    = np.flip(npmat[0:r, c ])
      right =        npmat[r, c+1:]
      down  =        npmat[r+1:, c]

      vis    = check_cell(r,c,mat,vis, left, up, down, right)

      print(f"checking {r},{c}")
      scenic = check_scenic(r,c,mat,scenic, left,up,down,right)
      #print(f"scenic {scenic}")

      #up   =  [ uprow[c]   for uprow   in mat[r-1:-1:-1] ]
      #down =  [ downrow[c] for downrow in mat[r:]        ]
      #left  = [ leftcol[c-1:-1:-1] for leftcol in mat[r]       ] 
      #right = [ rghtcol[c+1:] for rghtcol in mat[r]      ] 
      print(f"r {r} c {c} up is    {type(up)} {up} ")
      print(f"r {r} c {c} down is  {type(down)} {down}")
      print(f"r {r} c {c} left is  {type(left)} {left}")
      print(f"r {r} c {c} right is {type(right)} {right}")

  result = sum([ any(c) for r in vis for c in r ])
  npmat = np.array(mat)
  #print(f"mp slice {npmat[0:2, 46:48]}")
  print (f"part 1 result len is {result}")
  pprint(scenic)
  tmp = [ math.prod(c) for r in scenic for c in r ]
  print(len(tmp))
  result2 = max(tmp)
  #result2 = max([ reduce(lambda: x, y: x * y, c) for r in scenic for c in r ])
  print (f"part 2 result is {result2}") # first guess 1026: wrong

if __name__ == "__main__":
  main()
