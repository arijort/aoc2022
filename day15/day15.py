#!/usr/local/bin/python3.11
import re
import numpy as np
from bitarray import bitarray
filename = "input.txt"
#filename = "small"

"""
Part 1:

  Given positions of sensors and beacons, where each sensor indicates it's closest beacon,
  work out where beacons cannot be.

  In row y=2000000 how many positions cannot contain a beacon?

Part 2
"""

class sensor:
  def __init__(self, pos: tuple[int,int], bea: tuple[int,int] ) -> None:
    self.pos = pos
    self.px,self.py = pos
    self.bea = bea
    self.range = self.mnhn_dist(self.bea)

  def mnhn_dist(self, bea: tuple[int,int]) -> int:
    """ Produce Manhattan distance between the sensor and the beacon """
    return abs(self.pos[0] - bea[0]) + abs(self.pos[1] - bea[1])

  def in_range(self, point: tuple[int,int]) -> bool:
    return self.mnhn_dist(point) < self.range

  def coverage_borders(self) -> tuple[ tuple[bool,int] ]:
    """ Imagine cartesian grid, we return the 4 lines which mark the edges of the coverage area"""
    return ( *self.positive_borders() , *self.negative_borders() )
  def positive_borders(self) -> tuple[tuple[bool,int]]:
    border_tl = (True, # top left border has positive slope
                 self.py - self.px + self.range )
    border_br = (True, # bottom right border has positive slope
                 self.py - self.px - self.range )
    return (border_tl, border_br)
  def negative_borders(self) -> tuple[tuple[bool,int]]:
    border_tr = (False,
                 self.py + self.px + self.range)
    border_bl = (False,
                 self.py + self.px - self.range)

limit_min, limit_max = 0, 4_000_000
#limit_min, limit_max = 0, 20

def parse():
  #beacon_x, beacon_y = {},{}
  sensor_d = {}
  #beacons = set()
  with open(filename, "r") as fh:
    for line in fh.readlines():
      sense_re = r'.*at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): .* at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)'
      points = re.match(sense_re, line)
      if not points:
        continue
      g = points.group
      key = ( int(g('sx')), int(g('sy')) )
      bea = ( int(g('bx')), int(g('by')) )
      #beacons.add( bea )
      #beacon_x[ key ] = int(g('bx'))
      #beacon_y[ key ] = int(g('by'))
      s = sensor( key, bea )
      sensor_d[key] = s # key is tuple(px,py) of sensor location, value is sensor object
  #return (beacon_x, beacon_y, beacons, sensor_d)
  return (sensor_d)

def get_distances(beacon_x, beacon_y):
  distances = {}
  for sx,sy in beacon_x:
    #distance = abs(sx - beacon_x[(sx,sy)]) + abs(sy - beacon_y[(sx,sy)])
    #print(f"sensor {(sx,sy)} distance {distance}")
    distances[(sx,sy)] = abs(sx - beacon_x[(sx,sy)]) + abs(sy - beacon_y[(sx,sy)])
  return distances

def check_row(distances, row):
  s = set()
  for sx,sy in distances:
    vert_dist = abs(sy - row)
    if vert_dist > distances[ (sx,sy) ]:
      continue
    horiz_dist = distances[ (sx,sy) ] - vert_dist
    left  = sx - horiz_dist
    right = sx + horiz_dist
    s.update( list(range(left, right+1) ) )
  return s

def do_row(sensor_d, row) -> set: 
  """ return set of location in given row that cannot have a beacon. """
  s,b = set(), set()
  for sx, sy in sensor_d:
    key = (sx,sy)
    if sensor_d[key].bea[1] == row:
      b.add( sensor_d[key].bea )
    vert_dist = abs(sy - row)
    if vert_dist > sensor_d[key].range:
      continue
    horiz_dist = sensor_d[key].range - vert_dist
    left  = sx - horiz_dist
    right = sx + horiz_dist
    s.update( list(range(left, right+1) ) )
  return len(s) - len(b)

def part2(distances):
  rx, ry = 1,1
  result = 0
  b = bitarray(limit_max)
  for r in range(limit_max + 1):
    b.setall(0)
    for sx,sy in distances:
      vert_dist = abs(sy - r)
      if vert_dist > distances[ (sx,sy) ]:
        continue
      horiz_dist = distances[ (sx,sy) ] - vert_dist
      left  = max(limit_min, sx - horiz_dist)
      right = min(limit_max, sx + horiz_dist) + 1
      b[left:right] = 1

    try:
      i = b.index(0)
      print(f"found spot row {r} col {i}")
      result = i * limit_max + r
    except(ValueError):
      if r % 100000 == 0:
        print(f"no empty beacon spots in row {r}")
      continue
  return result

def main():
  row = 2_000_000
  #beacon_x, beacon_y, beacons, sensor_d = parse()
  sensor_d = parse()
  #distances = get_distances(beacon_x, beacon_y)
  #covered = check_row(distances, row)
  r1 = do_row(sensor_d, row)
  #r1 = len(covered)
  #for _,by in beacons:
  #  if by == row: r1 -= 1
  print(f"part 1: {r1}") # 4665948

  r2 = 0
  #for n in range(row-2_000_000, row+2_00_000):
  #for n in range(limit_max + 1):
  #covered = part2(distances)
  #if covered: r2 = covered
  print(f"part 2: {r2}")

if __name__ == "__main__":
  main()
