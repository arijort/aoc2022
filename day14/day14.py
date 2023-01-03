#!/usr/local/bin/python3.11
import sys
import numpy as np
from pprint import pprint
filename = "input.txt"
#filename = "small"

"""
Part 1:

Given coordinates of rock in form of lines (x1,y1) -> (x2,y2) and
given starting point of falling sand at (500,0);
identify how many sand units fall and come to rest before sand falls off into infinity

Part 2

Given a floor at max_y + 2, where max_y is the largest y value among the given points,
compute how many grains of sand fall before a unit comes to rest at the starting point
(500,0)
"""

def parse():
  cave,rocks = [],[]
  with open(filename, "r") as fh:
    for line in fh.readlines():
      rocks = [ rock for rock in line.strip().split(" -> ") ]
      points = [ tuple(map(int, rock.split(","))) for rock in rocks ]
      cave.append(points)
  return cave

def make_grid(cave):
  max_x, max_y = 0,0
  for line in cave:
    for px,py in line:
      max_x = max(max_x, px+210)
      max_y = max(max_y, py+3)
  #print(f"max x {max_x} y {max_y}")
  grid = np.ones( (max_y, max_x) )
  for line in cave:
    for n, seg in enumerate(line):
      if n == 0: continue
      startx, starty = line[n-1]
      endx, endy = seg
      if startx == endx: # vertical line
        starty, endy = min(starty, endy), max(starty, endy) + 1
        grid[starty:endy, startx] = 8
      elif starty == endy: # horizontal line
        startx, endx = min(startx, endx), max(startx, endx) + 1
        grid[starty, startx:endx] = 8
  return grid

def part1(grid):
  ct = 0
  while not dropsand(grid, 500, 0): ct += 1
  return ct

def part2(grid):
  grid[-1,] = 8 # create floor
  ct = 0 
  while not dropsand(grid, 500, 0, True): ct+=1
  return ct + 1 #to account for last sand

def dropsand(grid, dropx=500, dropy=0, checktop=False):
  result = False
  vector = grid[dropy:, dropx] # check vector from drop point going down
  stop, stopy = np.where(vector > 6), len(grid)
  if stop: # and stop[0]:
    if len(stop[0]) > 0:
      stopy = stop[0][0] - 1 + dropy
  if stopy >= len(grid): 
    result = True # fell off the bottom into abyss
  elif 0 < dropx and grid[stopy + 1, dropx - 1] == 1: # check left
    result = dropsand(grid, dropx - 1, stopy + 1)
  elif dropx < len(grid[0]) -1  and grid[stopy + 1, dropx + 1] == 1: # check right
    result = dropsand(grid, dropx + 1, stopy + 1)
  else:
    grid[stopy, dropx] = 7 # sand came to rest
    if checktop and (stopy, dropx) == (dropy,dropx): result = True # part 2
  return result

def main():
  cave = parse()
  grid = make_grid(cave)
  r1 = part1(grid)
  print(f"part 1: {r1}") # 763
  r2 = part2(grid)
  print(f"part 2: {r1+r2}") # 23921

if __name__ == "__main__":
  main()
