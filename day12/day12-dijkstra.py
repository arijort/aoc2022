import heapq
from math import inf

input = 'input.txt'
#input = 'small'
heights = {}
dirs = [ (1,0), (-1,0), (0,-1), (0,1) ]
climb_test = lambda h, px, py: h <= heights[ (px,py)] + 1
dscnd_test = lambda h, px, py: h >= heights[ (px,py)] - 1

def get_neighbors(pointr, pointc, move_test):
  neighbors = []
  for dr, dc in dirs:
    if 0 <= pointr + dr < len(grid) and 0 <= pointc + dc < len(grid[0]):
      if move_test( heights[ (pointr+dr, pointc+dc) ], pointr,pointc):
        neighbors.append( (pointr+dr, pointc+dc) )
  return neighbors

def do_dscnd(start, endch, move_test):
  """ there can be multiple endpoints. return them all """
  q, endpoints, costs = [], [], {}
  heapq.heappush(q, (0, start) )
  while q:
    cost, point = heapq.heappop(q)
    pr, pc = point
    if grid[pr][pc] == endch:
      costs[ point ] = min(cost, costs[point])
      endpoints.append(point)
      continue
    for n in get_neighbors( pr, pc, move_test):
      if costs.get(n, inf) > cost + 1:
        costs[n] = cost + 1
        heapq.heappush(q, (cost+1, n))
  return min( [ costs[p] for p in endpoints ] )

def do_climb(start, end, move_test):
  q, costs = [], {}
  heapq.heappush(q, (0, start) )
  while q: 
    cost, point = heapq.heappop(q)
    for n in get_neighbors( *point, move_test):
      if costs.get(n, inf) > cost + 1:
        costs[n] = cost + 1
        heapq.heappush(q, (cost+1,n))
  return costs.get(end, inf)

with open(input, 'r') as fh:
  grid = [ list(line.strip()) for line in fh.readlines() ]
  for x, row in enumerate(grid):
    for y, ch in enumerate(row):
      match ch:
        case 'S':
          start, ch = (x,y), 'a'
        case 'E':
          end, ch = (x,y), 'z'
      heights[ (x,y) ] = ord(ch)
print(do_climb(start, end, climb_test))
print(do_dscnd(end, 'a', dscnd_test))
