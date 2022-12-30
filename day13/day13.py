#!/usr/local/bin/python3.11
import sys
import numpy as np
from pprint import pprint
from functools import cmp_to_key
filename = "input.txt"
#filename = "small"

"""
Part 1:

Strings of [] pairs and numbers, determine whether the two pairs arrive in order.

Part 2

Find shortest path from any 'a' elevation sqaure to the end.

"""

def int_cmp(a,b):
  if a < b: return -1
  if a > b: return 1
  return 0
def do_check(left, right):
  # take a pair of instructions in array to determine if they are in the right order
  result = 0
  if not left: result = -1
  if type(left) == int == type(right):
    result = int_cmp(left, right)
  elif type(left) == list == type(right):
    ll, rl = len(left), len(right)
    for r in range(min(ll,rl)):
      result = do_check(left[r], right[r])
      if result:
        break
    else: result = int_cmp(ll, rl)
  elif type(left) == int:
    result = do_check([left], right)
  elif type(right) == int:
    result = do_check(left, [right])
  return result

def part2(instrs):
  first, second = [[2]], [[6]]
  instrs.extend([first, second])
  instrs = sorted(instrs, key=cmp_to_key(do_check))
  return (instrs.index(first) + 1) * (instrs.index(second) + 1)

def parse():
  instrs = []
  with open(filename, "r") as fh:
    for line in fh.readlines():
      if line != '\n':
        instrs.append( eval(str(line)))
  return instrs

def part1(lines):
  result, ct = 0, 1
  pairs = []
  for line in lines:
    pairs.append( line )
    if len(pairs) == 2:
      if do_check( pairs[0], pairs[1] ) == -1: result += ct
      pairs = []
      ct += 1
  return result

def main():
  lines = parse()
  r1 = part1(lines)
  r2 = part2(lines)
  print(f"part 1: {r1}") # 4894
  print(f"part 2: {r2}") # 24180

if __name__ == "__main__":
  main()
