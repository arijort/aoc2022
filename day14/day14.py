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

"""



def parse():
  cave,rocks = [],[]
  with open(filename, "r") as fh:
    for line in fh.readlines():
      points = [ rock.split(",") for rock in line.strip().split(" -> ") ]
      segments = []
      for p in points:
        i = [ int(coord) for coord in p ]
        segments.append(i)
      cave.append(segments)
  #pprint(cave)
  return cave

def part1(cave):
  ct = 0
  max_x, max_y = 0,0
  for line in cave:
    for px,py in line:
      max_x = max(max_x,px) + 2
      max_y = max(max_y,px) + 2

  print(f"max x {max_x} y {max_y}")
  grid = np.ones( (max_y, max_x) )
  for line in cave:
    for n, seg in enumerate(line):
      if n == 0: continue
      #print(f"make rock from {line[n-1]} to {seg}")
      startx, starty = line[n-1]
      endx, endy = seg
      # create ranges for np
      if startx == endx:
        starty, endy = min(starty, endy), max(starty, endy) + 1
        grid[starty:endy, startx] = 8
      elif starty == endy:
        startx, endx = min(startx, endx), max(startx, endx) + 1
        grid[starty, startx:endx] = 8
      #print(f"  rock from {startx},{starty} to {endx},{endy}")
      
  print(grid[0:40,493:505])
  lostsand = False
  while not lostsand:
    #print(f"itr {ct}")
    # start sand at 500,0
    lostsand = dropsand(grid, 500, 0)
    ct += 1
  #pprint(grid)
  print(grid[0:40,493:505])
  return ct - 1

def dropsand(grid, dropx=500, dropy=0):
  # range to check: 500,0:
  result = False
  #print(f"check vector {dropx},{dropy} ")
  vector = grid[dropy:, dropx]
  #print(f"have v {vector} {type(vector)}")
  stop, stopy = np.where(vector > 6), len(grid)
  #print(f"have stop {stop} {type(stop)}")
  #print(f"  {type(stop[0])}")
  #if not stop:
    #print(f"fell into abys")
  #  result = True
  if stop: # and stop[0]:
    if len(stop[0]) > 0:
      stopy = stop[0][0] - 1 + dropy
  #print(f"check {dropx-1},{stopy+1} and {dropx+1},{stopy+1}")
  if stopy >= len(grid): 
    print(f"fell into abys")
    result = True
  elif grid[stopy + 1, dropx - 1] == 1:
    #print(f"trying left {dropx -1} {stopy+1}")
    result = dropsand(grid, dropx - 1, stopy + 1)
  elif grid[stopy + 1, dropx + 1] == 1:
    #print(f"trying right")
    result = dropsand(grid, dropx + 1, stopy + 1)
  else:
    #print(f"  found rest point {dropx} {stopy}")
    grid[stopy, dropx] = 7
    #print(grid[0:11,493:505])
  #print(f"have index {np.where(vector == 8)[0][0]}")
  return result

def main():
  cave = parse()
  r1 = part1(cave)
  r2 = part2(cave)
  print(f"part 1: {r1}")
  #print(f"part 2: {r1+r2}")

if __name__ == "__main__":
  main()
