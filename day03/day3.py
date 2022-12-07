#!/usr/bin/env python

import os
import sys

filename = "input.txt"


"""
The list of items for each rucksack is given as characters all on a single line.
A given rucksack always has the same number of items in each of its two compartments, so the first half of the
characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

To help prioritize item rearrangement, every item type can be converted to a priority:

  Lowercase item types a through z have priorities 1 through 26.
  Uppercase item types A through Z have priorities 27 through 52.

Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?


Updated rules:
  Every set of three lines in your list corresponds to a single group, but each group can have a different badge item type
  Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?
"""

def get_prio(char):
  """
  Use ascii values to convert chars to prios:
    a->z => 1 through 26 iow subtract 96 ord('a') = 97 ord('z') = 122
    A->z => 27 through 52 iow subtract 38 ord('a') = 65 ord('z') = 90
  """
  if char.islower():
    return ord(char) - 96
  elif char.isupper():
    return ord(char) - 38
  else:
    return 0


def main():
  total_prios = 0
  with open(filename, "r") as fh:
    for line in fh:
      bisector = int(len(line) / 2) 
      first = set( i for i in line[:bisector] )
      second = set( i for i in line[bisector:] )

      prios = [ get_prio(i) for i in first.intersection(second) ]
      assert( 1 == len(prios))
      total_prios += prios[0] # assume 1
  print(f"total score is {total_prios} ")

def updated():
  total_prios = 0
  with open(filename, "r") as fh:
    for line in fh:
      first = set(line.strip())
      second = set(list(fh.readline().strip() ))
      third = set(list(fh.readline().strip() ))

      badge = [ get_prio(i) for i in first.intersection(second, third)]
      assert(1 == len(badge))
      total_prios += badge[0]

  print(f"updated score is {total_prios} ")

if __name__ == "__main__":
  main()
  updated()

