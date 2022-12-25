#!/usr/local/bin/python3.11

import sys
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
costs = []

climb_test = lambda ch, px, py: ord(ch) <= ord( grid[px][py]) + 1


def get_neighbors(px, py):
  neighbors = []
  #print(f"getting neighbors from {px},{py}")
  if px-1 >= 0 and ord(grid[px-1][py]) <= ord( grid[px][py] ) + 1:
    #print(f"  checking {px},{py} up")
    #print(f"  compared point {grid[px][py]} to neighbor {grid[px-1][py]}")
    neighbors.append( (px-1, py) )
  if px+1 < len(grid) and ord(grid[px+1][py]) <= ord( grid[px][py] ) + 1:
    #print(f"  checking {px},{py} down")
    #print(f"  compared point {grid[px][py]} to neighbor {grid[px+1][py]}")
    neighbors.append( (px+1, py) )
  if py-1 >= 0 and ord(grid[px][py-1]) <= ord( grid[px][py] ) + 1:
    #print(f"  checking {px},{py} left")
    #print(f"  compared point {grid[px][py]} to neighbor {grid[px][py-1]}")
    neighbors.append( (px, py-1) )
  if py+1 < len(grid[0]) and ord(grid[px][py+1]) <= ord( grid[px][py] ) + 1:
    #print(f"  checking {px},{py} right")
    #print(f"  compared point {grid[px][py]} to neighbor {grid[px][py+1]}")
    neighbors.append( (px, py+1) )

  #print(f"returning neighbors {neighbors}")
  return neighbors


def explore(startr, startc, endr, endc, grid):
  dfs = [] # stack of points for depth first search
  dfs.append( (startr, startc, 0) ) # initial cost

  while len(dfs) > 0:
    pointr, pointc, cost = dfs.pop()
    print(f"exploring from {pointr},{pointc} with cost {cost}")
    if pointr == endr and pointc == endc:
      costs[endr][endc] = cost
      continue
    if costs[pointr][pointc] <= cost:
      continue # ignore this point, already visited
    costs[pointr][pointc] = min(costs[pointr][pointc], cost)
    for pr,pc in get_neighbors(pointr, pointc):
      if costs[pr][pc] <= cost+1:
        continue
      #print(f"  pushing to stack {pr},{pc} with cost {cost+1}")
      dfs.append( (pr, pc, cost+1) )
      #print(f"  stack is {dfs}")
  

def main():
  #parse()

  with open(filename, "r") as fh:
    r = 0
    for line in fh:
      grid.append(list(line.strip()))
      costline = [sys.maxsize] * (len(line)  - 1)
      costs.append(costline)
      c = 0
      for ch in line:
        if ch == 'S':
          start = (r,c)
        elif ch == 'E':
          end = (r,c)
        c += 1        
      r += 1
  #pprint(grid)
  #print(f"have start {start} end {end}") 

  grid[start[0]][start[1]] = 'a'
  #costs[start[0]][start[1]] = 0
  grid[end[0]][end[1]] = 'z'
  explore(start[0], start[1], end[0], end[1], grid)
  print(f"have travel cost {costs[end[0]][end[1]] }")
  #pprint(costs)

if __name__ == "__main__":
  main()
