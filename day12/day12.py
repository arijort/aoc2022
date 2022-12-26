#!/usr/local/bin/python3.11
import sys
import numpy as np
from pprint import pprint
filename = "input.txt"
#filename = "small"

"""
Part 1:

  Given map of altitudes as below 'a' is lowest and 'z' is highest altitude.
  Find the shortest path from S to E. Constraint is that you can move up, down, left right and up maximum 1 unit of altitude.

  Sabqponm
  abcryxxl
  accszExk
  acctuvwj
  abdefghi

Part 2

Find shortest path from any 'a' elevation sqaure to the end.

"""

grid = [] 
heights = {}
costs = np.array(0)

climb_test   = lambda h, px, py: h <= heights[(px,py)] + 1
descend_test = lambda h, px, py: h >= heights[(px,py)] - 1

dirs = [ (1,0), (-1,0), (0,1), (0,-1) ]

def get_neighbors(px, py, move_test):
  neighbors = []
  for dr, dc in dirs:
    if 0 <= px + dr < len(grid) and 0 <= py + dc < len(grid[0]):
      if move_test( heights[ (px+dr, py+dc) ], px, py):
        neighbors.append( (px+dr, py+dc) )
  return neighbors

def explore_any_startpoints(startr, startc, endr, endc, grid, move_test):
  dfs = []
  dfs.append( (startr,startc,0) )
  startpoints = set()
  while dfs:
    pointr,pointc,cost = dfs.pop()
    if grid[pointr][pointc] == 'a':
      costs[pointr][pointc] = min(costs[pointr][pointc], cost)
      startpoints.add( (pointr,pointc) )
      continue
    if costs[pointr][pointc] <= cost:
      continue # ignore this point, already visited
    costs[pointr][pointc] = min(costs[pointr][pointc], cost)
    for pr,pc in get_neighbors(pointr,pointc, move_test):
      if costs[pr][pc] <= cost + 1:
        continue
      dfs.append( (pr,pc,cost+1) )
  return startpoints

def explore(startr, startc, endr, endc, grid, move_test):
  dfs = [] # stack of points for depth first search
  dfs.append( (startr, startc, 0) ) # initial cost

  while len(dfs) > 0:
    pointr, pointc, cost = dfs.pop()
    #print(f"exploring from {pointr},{pointc} with cost {cost}")
    if pointr == endr and pointc == endc:
      costs[endr][endc] = cost
      continue
    if costs[pointr][pointc] <= cost:
      continue # ignore this point, already visited
    costs[pointr][pointc] = min(costs[pointr][pointc], cost)
    for pr,pc in get_neighbors(pointr, pointc, move_test):
      if costs[pr][pc] <= cost+1:
        continue
      dfs.append( (pr, pc, cost+1) )

def parse():
  with open(filename, "r") as fh:
    grid = [ list(line.strip()) for line in fh.readlines() ]
  return grid

def main():
  global grid,costs
  grid = parse()
  for x, row in enumerate(grid):
    for y, ch in enumerate(row):
      match ch:
        case 'S':
          start = (x, y)
          ch = 'a'
        case 'E':
          end = (x, y)
          ch = 'z'
      heights[ (x,y) ] = ord(ch)

  costs = np.zeros(shape=( len(grid), len(grid[0]))) + sys.maxsize
  explore(start[0], start[1], end[0], end[1], grid, climb_test)
  r1 = costs[end[0]][end[1]] 
  costs = np.zeros(shape=( len(grid), len(grid[0]))) + sys.maxsize
  startpoints = explore_any_startpoints (end[0], end[1], start[0], start[1], grid, descend_test)
  min_startpoints = min([ costs[pr][pc] for pr,pc in startpoints ])

  print(f"part 1 travel cost {r1}")
  print(f"part 2 travel cost {min_startpoints}")

if __name__ == "__main__":
  main()
