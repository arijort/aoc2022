#!/usr/bin/env python

import os
import sys

filename = "input.txt"


"""
Some of the pairs have noticed that one of their assignments fully contains the other.
For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6.

In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, 
so these seem like the most in need of reconsideration.

In how many assignment pairs does one range fully contain the other?

Example input:
  99-99,18-99
  2-86,1-86
  9-21,10-22
  1-24,7-23
  33-37,35-38
  15-57,14-56
  1-88,3-89
  26-56,27-57
  11-94,93-98
  40-92,3-91
"""


def main():
  total = 0
  with open(filename, "r") as fh:
    for line in fh:
      (first, second) = line.split(",")
      (first_start, first_end)   = [ int(i) for i in first.split("-") ]
      (second_start, second_end) = [ int(i) for i in second.split("-") ]

      if first_start <= second_start and first_end >= second_end:
        total += 1
      elif int(first_start) >= int(second_start) and first_end <= second_end:
        total += 1

  print(f"total is {total} ")

def updated():
  """
  In how many segments is there any overlap at all?
  """
  total = 0
  with open(filename, "r") as fh:
    for line in fh:
      (first, second) = line.split(",")
      (first_start, first_end)   = [ int(i) for i in first.split("-") ]
      (second_start, second_end) = [ int(i) for i in second.split("-") ]
      if second_start <= first_start <= second_end or first_start <= second_start <= first_end:
        total += 1

  print(f"updated score is {total} ")

if __name__ == "__main__":
  main()
  updated()

