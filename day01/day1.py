#!/usr/bin/env python

import os 
import sys

filename = "input.txt"

max_size = sys.maxsize
min_size = -sys.maxsize - 1


"""
Elves write their inventory in a single list like this. Each grouping represents the items each elf is carrying.
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
"""

def main():
  result = 0
  max_cal = min_size
  with open(filename, "r") as fh:

    elf_total = 0
    for line in fh:
      if line == '\n':
        max_cal = max(max_cal, elf_total)
        elf_total = 0
      else:
        elf_total += int(line)
        
  print(max_cal)

if __name__ == "__main__":
  main()

